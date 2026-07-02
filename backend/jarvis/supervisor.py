from __future__ import annotations

from dataclasses import asdict, dataclass, field

from backend.jarvis.registry import JarvisAgent, get_agent
from backend.jarvis.router import JarvisRouter


@dataclass
class SupervisorStep:
    order: int
    agent_key: str
    agent_name: str
    role: str
    voice: str
    tone: str
    model_policy: str
    instruction: str


@dataclass
class SupervisorPlan:
    supervisor: str
    task: str
    primary_agent: str
    steps: list[SupervisorStep] = field(default_factory=list)
    final_response_contract: str = "Jarvis sintetizza il lavoro degli specialisti in una risposta breve, chiara e orientata alla prossima azione."

    def to_dict(self) -> dict[str, object]:
        return {
            "supervisor": self.supervisor,
            "task": self.task,
            "primary_agent": self.primary_agent,
            "steps": [asdict(step) for step in self.steps],
            "final_response_contract": self.final_response_contract,
        }


class JarvisSupervisor:
    """Supervisor pattern: Jarvis selects specialists and owns the final response."""

    def __init__(self) -> None:
        self.router = JarvisRouter()
        self.jarvis = get_agent("jarvis")

    def build_plan(self, task: str) -> SupervisorPlan:
        primary = self.router.select_agent(task)
        selected = self._select_sequence(task, primary)
        steps = [self._make_step(index + 1, agent, task) for index, agent in enumerate(selected)]
        return SupervisorPlan(
            supervisor=self.jarvis.name,
            task=task,
            primary_agent=primary.key,
            steps=steps,
        )

    def supervisor_prompt(self, task: str) -> str:
        plan = self.build_plan(task)
        lines = [
            "# Jarvis Supervisor Plan",
            "",
            f"Task: {task}",
            f"Supervisor: {plan.supervisor}",
            f"Primary agent: {plan.primary_agent}",
            "",
            "## Specialist sequence",
        ]
        for step in plan.steps:
            lines.append(
                f"{step.order}. {step.agent_name} ({step.role}) - voice={step.voice}, tone={step.tone}, model={step.model_policy}\n   Instruction: {step.instruction}"
            )
        lines.extend(
            [
                "",
                "## Final response rule",
                plan.final_response_contract,
            ]
        )
        return "\n".join(lines)

    def _select_sequence(self, task: str, primary: JarvisAgent) -> list[JarvisAgent]:
        text = task.lower()
        sequence: list[JarvisAgent] = [primary]

        if primary.key in {"coder", "architect"}:
            sequence.append(get_agent("reviewer"))

        if any(word in text for word in {"security", "sicurezza", "token", "auth", "permessi", "deploy"}):
            sequence.append(get_agent("security"))

        if any(word in text for word in {"docs", "documenta", "readme", "guida"}):
            sequence.append(get_agent("docs"))

        if any(word in text for word in {"release", "deploy", "rilascio", "changelog"}):
            sequence.append(get_agent("release"))

        deduped: dict[str, JarvisAgent] = {}
        for agent in sequence:
            deduped[agent.key] = agent
        return list(deduped.values())

    @staticmethod
    def _make_step(order: int, agent: JarvisAgent, task: str) -> SupervisorStep:
        return SupervisorStep(
            order=order,
            agent_key=agent.key,
            agent_name=agent.name,
            role=agent.role,
            voice=agent.voice,
            tone=agent.tone,
            model_policy=agent.model_policy,
            instruction=f"Gestisci il task dal punto di vista {agent.role}: {task}",
        )
