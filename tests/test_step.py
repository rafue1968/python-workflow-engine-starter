from app.engine.step import Step


def test_step_success():
    step = Step("ok", lambda: 42)
    assert step.run() == 42


def test_step_retry():
    attempts = {"count": 0}

    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("fail once")
        return "ok"

    step = Step("retry", flaky, retries=1)
    assert step.run() == "ok"
