from __future__ import annotations

from orchestrator.models import AgentRole, AgentSpec


AGENT_REGISTRY: dict[AgentRole, AgentSpec] = {
    AgentRole.ARCHITECT: AgentSpec(
        role=AgentRole.ARCHITECT,
        name="Architect Agent",
        mission="Trasforma richieste vaghe in piani tecnici verificabili.",
        prompt_path="prompts/architect.md",
    ),
    AgentRole.CODER: AgentSpec(
        role=AgentRole.CODER,
        name="Coder Agent",
        mission="Implementa modifiche piccole, sicure e testabili.",
        prompt_path="prompts/coder.md",
        can_write_code=True,
    ),
    AgentRole.REVIEWER: AgentSpec(
        role=AgentRole.REVIEWER,
        name="Reviewer Agent",
        mission="Controlla qualità, regressioni e mantenibilità.",
        prompt_path="prompts/reviewer.md",
    ),
    AgentRole.SECURITY: AgentSpec(
        role=AgentRole.SECURITY,
        name="Security Agent",
        mission="Cerca rischi, segreti, permessi e comandi pericolosi.",
        prompt_path="prompts/security.md",
    ),
    AgentRole.RELEASE: AgentSpec(
        role=AgentRole.RELEASE,
        name="Release Agent",
        mission="Prepara changelog, PR e note di rilascio.",
        prompt_path="prompts/release.md",
        can_release=True,
    ),
    AgentRole.DOCS: AgentSpec(
        role=AgentRole.DOCS,
        name="Docs Agent",
        mission="Aggiorna documentazione e istruzioni operative.",
        prompt_path="prompts/docs.md",
        can_write_code=True,
    ),
}


def get_agent(role: AgentRole) -> AgentSpec:
    return AGENT_REGISTRY[role]
