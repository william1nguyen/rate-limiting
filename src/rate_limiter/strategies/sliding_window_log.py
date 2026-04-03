import time
import threading
from collections import deque


class SlidingWindowLog:

    def __init__(self, window_size: float, limit: int):
        assert window_size > 0
        assert limit > 0

        self.window_size = window_size
        self.limit = limit
        self.logs: deque[tuple[float, int]] = deque()

        self._current_count: int = 0
        self.lock = threading.Lock()

    def _cleanup(self, now: float) -> None:
        cutoff = now - self.window_size
        while self.logs and self.logs[0][0] < cutoff:
            _, tokens = self.logs.popleft()
            self._current_count = max(0, self._current_count - tokens)

    def allow_request(self, required_tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            self._cleanup(now)

            if self._current_count + required_tokens > self.limit:
                return False

            self.logs.append((now, required_tokens))
            self._current_count += required_tokens

            return True

    def get_remaining(self) -> int:
        with self.lock:
            now = time.time()
            self._cleanup(now)

            return max(0, self.limit - self._current_count)

    def get_reset_time(self) -> float:
        with self.lock:
            if not self.logs:
                return time.time()

            return self.logs[0][0] + self.window_size
