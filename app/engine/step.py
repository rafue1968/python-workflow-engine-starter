from typing import Callable, Any
from app.engine.status import StepStatus

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
        self.status = StepStatus.PENDING

    def run(self) -> Any:
        self.status = StepStatus.RUNNING
        while self.attempts <= self.retries:
            try:
                self.attempts += 1
                result = self.func()
                self.status = StepStatus.SUCCESS
                return result
            except Exception as e:
                self.last_error = e
                if self.attempts > self.retries:
                    self.status = StepStatus.FAILED
                    raise