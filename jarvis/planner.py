from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from jarvis.supervisor import JarvisSupervisor


@dataclass
class FlightStep:
    step_id: int
    assigned_agent: str
    action: str
    objective: str
    parameters: dict[str, str] = field(default_factory=dict)
    depends_on: list[int] = field(default_factory=list)
    success_criteria: str = ""


@dataclass
class FlightPlan:
    command_intent: str
    created_at: str
    planner_policy: str
    steps: list[FlightStep]
    final_response: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "command_intent": self.command_intent,
            "created_at": self.created_at,
            "planner_policy": self.planner_policy,
            "steps": [asdict(step) for step in self.steps],
            "final_response": self.final_response,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class FlightPlanner:
    """Deterministic fallback planner for the Supervisor-Executor architecture.

    A top-tier reasoning model can replace this later by returning the same JSON contract.
    """

    def __init__(self, planner_policy: str = "reasoning-heavy-planner") -> None:
        self.supervisor = JarvisSupervisor()
        self.planner_policy = planner_policy

    def build(self, task: str, repository: str | None = None, repo_path: str | None = None) -> FlightPlan:
        supervisor_plan = self.supervisor.build_plan(task)
        steps: list[FlightStep] = []
        previous_id: int | None = None
        for index, supervisor_step in enumerate(supervisor_plan.steps, start=1):
            step = FlightStep(
                step_id=index,
                assigned_agent=supervisor_step.agent_key,
                action=self._action_for(supervisor_step.agent_key),
                objective=supervisor_step.instruction,
                parameters={
                    "repository": repository or "",
                    "repo_path": repo_path or "",
                    "model_policy": supervisor_step.model_policy,
                    "voice": supervisor_step.voice,
                },
                depends_on=[previous_id] if previous_id else [],
                success_criteria=self._success_for(supervisor_step.agent_key),
            )
            steps.append(step)
            previous_id = index

        return FlightPlan(
            command_intent=self._intent(task),
            created_at=datetime.now(timezone.utc).isoformat(),
            planner_policy=self.planner_policy,
            steps=steps,
            final_response={
                "agent_name": "Jarvis",
                "speech_output": "Piano creato. Jarvis coordina gli specialisti e restituisce una sintesi finale.",
                "voice_tone": "executive",
            },
        )

    @staticmethod
    def _intent(task: str) -> str:
        normalized = "_".join(task.lower().strip().split())[:80]
        return normalized or "unknown_intent"

    @staticmethod
    def _action_for(agent_key: str) -> str:
        actions = {
            "architect": "analyze_architecture_and_plan",
            "coder": "implement_atomic_change",
            "reviewer": "review_output_and_find_risks",
            "security": "check_security_constraints",
            "docs": "update_documentation",
            "release": "prepare_release_notes",
            "jarvis": "coordinate_and_summarize",
        }
        return actions.get(agent_key, "execute_specialist_task")

    @staticmethod
    def _success_for(agent_key: str) -> str:
        criteria = {
            "architect": "piano tecnico chiaro con vincoli e rischi",
            "coder": "modifica atomica, verificabile e testabile",
            "reviewer": "criticita e regressioni identificate",
            "security": "nessun rischio bloccante non mitigato",
            "docs": "documentazione aggiornata e coerente",
            "release": "rilascio descrivibile con changelog e checklist",
        }
        return criteria.get(agent_key, "output utile e verificabile")
