import time
import threading


class TokenBucket:
    def __init__(self, max_tokens: int, refill_rate: int, interval: float):
        assert max_tokens > 0
        assert refill_rate > 0
        assert interval > 0

        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.interval = interval

        self.tokens = max_tokens
        self.refill_at = time.time()
        self.lock = threading.Lock()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.refill_at

        if elapsed < self.interval:
            return

        num_refills = elapsed // self.interval
        self.tokens = min(self.max_tokens, self.tokens + num_refills * self.refill_rate)
        self.refill_at += num_refills * self.interval

    def allow_request(self, required_tokens: int = 1) -> bool:
        with self.lock:
            self._refill()

            if self.tokens >= required_tokens:
                self.tokens -= required_tokens
                return True

            return False

    def get_remaining(self) -> int:
        with self.lock:
            self._refill()
            return self.tokens

    def get_reset_time(self) -> float:
        with self.lock:
            return self.refill_at + self.interval
