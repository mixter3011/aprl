# tests/test_core.py

import time
import unittest
from aprl.core import RateLimiter

class TestRateLimiter(unittest.TestCase):

    def test_initialization(self):
        rate_limiter = RateLimiter(rate_limit=5, per_seconds=10)
        self.assertEqual(rate_limiter.rate_limit, 5)
        self.assertEqual(rate_limiter.per_seconds, 10)
        self.assertEqual(rate_limiter.allowance, 5)

    def test_acquire(self):
        rate_limiter = RateLimiter(rate_limit=2, per_seconds=1)
        
        start = time.time()
        rate_limiter.acquire()
        rate_limiter.acquire()
        rate_limiter.acquire()  
        end = time.time()

        self.assertGreater(end - start, 0.5)

if __name__ == '__main__':
    unittest.main()
