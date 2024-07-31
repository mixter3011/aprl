# aprl/config.py

class RateLimitConfig:
    def __init__(self, rate_limit, per_seconds):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
