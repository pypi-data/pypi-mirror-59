# -*- coding: future_fstrings -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
import threading

from common.logger import get_logger

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class ClientMixin(object):

    RETRIED_STATUS_CODES = [502, 503, 504, 429]

    @classmethod
    def get_new_session(cls, MAX_RETRY=3, BACKOFF_FACTOR=0.1):
        sess = requests.Session()
        retries = Retry(total=MAX_RETRY, backoff_factor=BACKOFF_FACTOR, status_forcelist=cls.RETRIED_STATUS_CODES)
        sess.mount('https://', HTTPAdapter(max_retries=retries))
        sess.mount('http://', HTTPAdapter(max_retries=retries))
        return sess

    @classmethod
    def make_request(cls, url, method="get", session=None, TIMEOUT=5,  is_file=False, logger=None, MAX_RETRY=3, BACKOFF_FACTOR=0.1, **kwargs):
        log = get_logger(__name__) if logger is None else logger
        start_time = datetime.now()
        sess = session if session else cls.get_new_session(MAX_RETRY, BACKOFF_FACTOR)
        try:
            resp = getattr(sess, method)(url, timeout=TIMEOUT, **kwargs)
            if 400 <= resp.status_code < 600:
                resp.reason = resp.text if resp.text else resp.reason
            resp.raise_for_status()
            log.debug(f'''MethodType: {method} Request url: {url} status_code: {resp.status_code}''')
            if resp.status_code == 200:
                if is_file:
                    data = resp.content
                else:
                    data = resp.json() if len(resp.content) > 0 else {}
                return True, data
            else:
                log.error(f'''Request Failed: {resp.content} url: {url} status_code: {resp.status_code} reason: {resp.reason}''')
                return False, resp.content
        except JSONDecodeError as err:
            log.error(f'''Error in Decoding response {err}''', exc_info=True)
        except requests.exceptions.HTTPError as err:
            log.error(f'''Http Error: {err}  {kwargs}''', exc_info=True)
        except requests.exceptions.ConnectionError as err:
            log.error(f'''Connection Error:{err}  {kwargs}''', exc_info=True)
        except requests.exceptions.Timeout as err:
            time_elapsed = datetime.now() - start_time
            log.error(f'''Timeout Error:{err}  {kwargs} {time_elapsed}''', exc_info=True)
        except requests.exceptions.RequestException as err:
            log.error(f'''Error: {err}  {kwargs}''', exc_info=True)
        finally:
            if not session:
                # if session was not input then deleting the current session
                sess.close()
        return False, ""


class SessionPool(object):
    # by default request library will not timeout for any request
    # session is not thread safe hence each thread gets new session
    def __init__(self, max_retry, backoff, logger=None):
        self.sessions = {}
        self.max_retry = max_retry
        self.backoff = backoff
        self.log = get_logger(__name__) if logger is None else logger
        self.total_sessions_created = 0
        self.total_sessions_deleted = 0

    def get_thread_id(self):
        try:
            thread_id = threading.get_ident()
        except AttributeError:
            thread_id = threading._get_ident()
        return thread_id

    def get_request_session(self):
        thread_id = self.get_thread_id()
        if thread_id in self.sessions:
            return self.sessions[thread_id]
        else:
            self.log.debug(f'''Creating session for {thread_id}''')
            sess = ClientMixin.get_new_session(self.max_retry, self.backoff)
            self.sessions[thread_id] = sess
            self.total_sessions_created += 1
            return sess

    def closeall(self):
        self.log.debug("Closing all sessions")
        for _, v in self.sessions.items():
            self.total_sessions_deleted += 1
            v.close()
        self.log.info(f'''Total sessions present: {len(self.sessions.keys())} Total sessions created: {self.total_sessions_created} Total sessions deleted: {self.total_sessions_deleted}''')

    def close(self):
        thread_id = self.get_thread_id()
        self.log.debug(f'Deleting session for {thread_id}')
        if thread_id in self.sessions:
            self.sessions[thread_id].close()
            del self.sessions[thread_id]
            self.total_sessions_deleted += 1
