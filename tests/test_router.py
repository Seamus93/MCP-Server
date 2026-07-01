from jarvis.supervisor import JarvisSupervisor


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


def test_supervisor_outputs_primary_agent() -> None:
    plan = JarvisSupervisor().build_plan("Progetta architettura per Jarvis")
    assert plan.supervisor == "Jarvis"
    assert plan.primary_agent == "architect"
