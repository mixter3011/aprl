# aprl/core.py

import time
from threading import Lock

class RateLimiter:
    def __init__(self, rate_limit: int, per_seconds: int):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.tokens = rate_limit
        self.lock = Lock()
        self.last_refill = time.time()

    def acquire(self):
        with self.lock:
            current_time = time.time()
            time_passed = current_time - self.last_refill

            if time_passed > self.per_seconds:
                self.tokens = self.rate_limit
                self.last_refill = current_time

            if self.tokens > 0:
                self.tokens -= 1
            else:
                time_to_wait = self.per_seconds - time_passed
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
                self.last_refill = time.time()
                self.tokens = self.rate_limit - 1
