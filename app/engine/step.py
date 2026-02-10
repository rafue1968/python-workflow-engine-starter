from typing import Callable, Any

class Step:
    def __init__(
            self,
            step_id: str,
            func: Callable[[], Any],
            retries: int = 0,
        ):
        self.step_id = step_id
        self.func = func
        self.retries = retries
        self.attempts = 0
        self.last_error: Exception | None = None

    def run(self) -> Any:
        while self.attempts <= self.retries:
            try:
                self.attempts += 1
                result = self.func()
                return result
            except Exception as e:
                self.last_error = e
                if self.attempts > self.retries:
                    raise