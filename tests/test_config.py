# tests/test_config.py

import unittest
from aprl.config import RateLimitConfig

class TestRateLimitConfig(unittest.TestCase):

    def test_initialization(self):
        config = RateLimitConfig(rate_limit=5, per_seconds=10)
        self.assertEqual(config.rate_limit, 5)
        self.assertEqual(config.per_seconds, 10)

if __name__ == '__main__':
    unittest.main()
