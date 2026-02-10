from app.engine.step import Step
from app.engine.workflow import Workflow

def step_a():
    print("Doing A")


def step_b():
    print("Doing B")

def step_c():
    raise ValueError("boom")

wf = Workflow("demo")

wf.add_step(Step("A", step_a))
wf.add_step(Step("B", step_b), depends_on=["A"])
wf.add_step(Step("C", step_c), depends_on=["B"])

wf.run()