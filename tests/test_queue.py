# tests/test_queue.py

import unittest
import time
from aprl.queue import RateLimitedQueue
from aprl.core import RateLimiter

class TestRateLimitedQueue(unittest.TestCase):

    def test_put(self):
        rate_limiter = RateLimiter(rate_limit=2, per_seconds=1)
        rate_limited_queue = RateLimitedQueue(rate_limiter)

        def dummy_task():
            pass

        start = time.time()
        rate_limited_queue.put(dummy_task)
        rate_limited_queue.put(dummy_task)
        rate_limited_queue.put(dummy_task)  
        rate_limited_queue.queue.join()  
        end = time.time()

        self.assertGreater(end - start, 0.5)  

if __name__ == '__main__':
    unittest.main()
