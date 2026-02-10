from collections import defaultdict, deque
from typing import Dict, List, Set

from app.engine.step import Step

class Workflow:
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.steps: Dict[str, Step] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)

    def add_step(self, step: Step, depends_on: List[str] | None = None) -> None:
        if step.step_id in self.steps:
            raise ValueError(f"Step `{step.step_id} already exists")
        
        self.steps[step.step_id] = step

        if depends_on:
            for dep in depends_on:
                if dep not in self.steps:
                    raise ValueError(f"Dependency '{dep}' does not exist")
                self.dependencies[step.step_id].add(dep)

    def _topological_sort(self) -> List[str]:
        in_degree = {step_id: 0 for step_id in self.steps}

        for step, deps in self.dependencies.items():
            for dep in deps:
                in_degree[step] += 1

        queue = deque([s for s, d in in_degree.items() if d == 0])
        ordered = []

        while queue:
            current = queue.popleft()
            ordered.append(current)

            for step, deps in self.dependencies.items():
                if current in deps:
                    in_degree[step] -= 1
                    if in_degree[step] == 0:
                        queue.append(step)
        
        if len(ordered) != len(self.steps):
            raise ValueError("Workflow contains a cycle")
        
        return ordered
    
    def run(self) -> None:
        order = self._topological_sort()

        for step_id in order:
            step = self.steps[step_id]
            print(f"→ Running step {step.step_id}")
            try:
                step.run()
                print(f"✓ Step {step.step_id} completed")
            except Exception:
                print(f"✗ Step {step.step_id} failed")
                raise