from __future__ import annotations

from backend.jarvis.planner import FlightPlan, FlightStep


class PlanExecutor:
    """Executor skeleton for flight plans.

    The current MVP does not execute destructive operations. It validates the plan and
    returns the ordered specialist work packages. Real execution can be added per tool.
    """

    def prepare_work_packages(self, plan: FlightPlan) -> list[dict[str, object]]:
        return [self._package(step) for step in plan.steps]

    @staticmethod
    def _package(step: FlightStep) -> dict[str, object]:
        return {
            "step_id": step.step_id,
            "agent": step.assigned_agent,
            "action": step.action,
            "objective": step.objective,
            "parameters": step.parameters,
            "depends_on": step.depends_on,
            "success_criteria": step.success_criteria,
            "status": "planned",
        }
