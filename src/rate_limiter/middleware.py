import threading
from typing import Callable

from rate_limiter.types import RateLimiter


class RateLimit:
    def __init__(self, factory: Callable[[str], RateLimiter]):
        self._factory = factory
        self._buckets: dict[str, RateLimiter] = {}
        self._lock = threading.Lock()

    def get_bucket(self, key: str) -> RateLimiter:
        if key not in self._buckets:
            with self._lock:
                self._buckets[key] = self._factory(key)
        return self._buckets[key]

    def allow_request(self, key: str, required_tokens: int = 1) -> bool:
        return self.get_bucket(key).allow_request(required_tokens)

    def get_remaining(self, key: str) -> int:
        return self.get_bucket(key).get_remaining()

    def get_reset_time(self, key: str) -> int:
        return self.get_bucket(key).get_reset_time()
