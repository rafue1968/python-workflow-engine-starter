from app.engine.step import Step
from app.engine.workflow import Workflow

def text_workflow_execution_order():
    executed = []

    def make_step(name):
        return Step(name, lambda: executed.append(name))
    
    wf = Workflow("test")


    wf.add_step(make_step("A"))
    wf.add_step(make_step("B"), depends_on=["A"])
    wf.add_step(make_step("C"), depends_on=["B"])

    wf.run()

    assert executed == ["A", "B", "C"]


def test_workflow_parallel_dependencies():
    executed = []

    wf = Workflow("parallel")

    wf.add_step(Step("A", lambda: executed.append("A")))
    wf.add_step(Step("B", lambda: executed.append("B")), depends_on=["A"])
    wf.add_step(Step("C", lambda: executed.append("C")), depends_on=["A"])

    wf.run()

    assert executed[0] == "A"
    assert set(executed[1:]) == {"B", "C"}

def test_workflow_cycle_detection():
    wf = Workflow("cycle")

    wf.add_step(Step("A", lambda: None))
    wf.add_step(Step("B", lambda: None), depends_on=["A"])

    wf.dependencies["A"].add("B")

    try:
        wf.run()
        assert False, "Expected cycle detection"
    except ValueError:
        pass