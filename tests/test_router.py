from backend.jarvis.supervisor import JarvisSupervisor
from backend.jarvis.router import JarvisRouter


def agent_keys(task: str) -> list[str]:
    return [step.agent_key for step in JarvisSupervisor().build_plan(task).steps]


def test_coding_task_uses_coder_and_reviewer() -> None:
    keys = agent_keys("Implementa un parser per il workflow")
    assert "coder" in keys
    assert "reviewer" in keys


def test_security_task_adds_security() -> None:
    keys = agent_keys("Controlla auth token e permessi")
    assert "security" in keys


def test_docs_task_adds_docs() -> None:
    keys = agent_keys("Documenta il nuovo endpoint nel readme")
    assert "docs" in keys


def test_deploy_task_uses_devops_security_and_review() -> None:
    keys = agent_keys("Verifica docker, pipeline e deploy su VPS")
    assert "devops" in keys
    assert "security" in keys
    assert "reviewer" in keys


def test_research_task_uses_research_agent() -> None:
    keys = agent_keys("Ricerca fonti aggiornate per integrazione Google Home")
    assert "research" in keys


def test_router_returns_model_and_authorized_mcps() -> None:
    decision = JarvisRouter().route_payload("Correggi docker e testa il deploy")

    assert decision["provider"] == "openai"
    assert decision["model"] == "ops-structured"
    assert "docker" in decision["mcps"]
    assert "docker_build" in decision["tools"]


def test_supervisor_outputs_primary_agent() -> None:
    plan = JarvisSupervisor().build_plan("Progetta architettura per Jarvis")
    assert plan.supervisor == "Jarvis"
    assert plan.primary_agent == "architect"
