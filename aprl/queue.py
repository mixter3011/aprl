# aprl/queue.py

import threading
import queue
import http.client
import ssl
import certifi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RateLimitedQueue:
    def __init__(self, rate_limiter, api_base_url):
        self.rate_limiter = rate_limiter
        self.queue = queue.Queue()
        self.api_base_url = api_base_url
        self.worker = threading.Thread(target=self._worker)
        self.worker.daemon = True
        self.worker.start()

    def _worker(self):
        while True:
            task, method, endpoint, headers, body = self.queue.get()
            self.rate_limiter.acquire()
            try:
                task(method, endpoint, headers, body)
            finally:
                self.queue.task_done()

    def put(self, task, method, endpoint, headers, body=None):
        full_endpoint = f"{self.api_base_url}{endpoint}"
        self.queue.put((task, method, full_endpoint, headers, body))
