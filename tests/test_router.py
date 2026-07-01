from orchestrator.models import AgentRole, TaskRequest
from orchestrator.router import TaskRouter


def roles_for(task: str, risk_level: str = "normal") -> list[AgentRole]:
    routed = TaskRouter().route(TaskRequest(title=task, description=task, risk_level=risk_level))
    return [agent.role for agent in routed.agents]


def test_architect_is_always_included() -> None:
    assert AgentRole.ARCHITECT in roles_for("Capisci questa richiesta")


def test_code_task_adds_coder_and_reviewer() -> None:
    roles = roles_for("Implement feature per login")
    assert AgentRole.CODER in roles
    assert AgentRole.REVIEWER in roles


def test_high_risk_adds_security() -> None:
    roles = roles_for("Aggiorna OAuth token flow", risk_level="high")
    assert AgentRole.SECURITY in roles


def test_release_task_adds_release_agent() -> None:
    roles = roles_for("Prepara changelog e release")
    assert AgentRole.RELEASE in roles
