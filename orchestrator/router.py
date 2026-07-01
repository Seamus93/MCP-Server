from __future__ import annotations

from orchestrator.models import AgentRole, RoutedTask, TaskRequest
from orchestrator.registry import get_agent


SECURITY_KEYWORDS = {
    "auth",
    "token",
    "secret",
    "password",
    "permission",
    "oauth",
    "api key",
    "deploy",
}

DOCS_KEYWORDS = {"readme", "docs", "documentation", "manual", "guide"}
RELEASE_KEYWORDS = {"release", "version", "changelog", "tag", "deploy"}
CODE_KEYWORDS = {"fix", "bug", "feature", "implement", "refactor", "test", "code"}


class TaskRouter:
    """Rule-based router for early-stage agent orchestration."""

    def route(self, request: TaskRequest) -> RoutedTask:
        text = f"{request.title} {request.description}".lower()
        roles: list[AgentRole] = [AgentRole.ARCHITECT]
        notes: list[str] = ["Architect sempre incluso per chiarire piano e confini."]

        if self._contains_any(text, CODE_KEYWORDS):
            roles.append(AgentRole.CODER)
            roles.append(AgentRole.REVIEWER)
            notes.append("Richiesta tecnica: Coder + Reviewer inclusi.")

        if self._contains_any(text, SECURITY_KEYWORDS) or request.risk_level == "high":
            roles.append(AgentRole.SECURITY)
            notes.append("Rischio sicurezza rilevato: Security incluso.")

        if self._contains_any(text, DOCS_KEYWORDS):
            roles.append(AgentRole.DOCS)
            notes.append("Documentazione coinvolta: Docs incluso.")

        if self._contains_any(text, RELEASE_KEYWORDS):
            roles.append(AgentRole.RELEASE)
            notes.append("Rilascio/versioning rilevato: Release incluso.")

        deduped_roles = list(dict.fromkeys(roles))
        agents = [get_agent(role) for role in deduped_roles]
        return RoutedTask(request=request, agents=agents, execution_notes=notes)

    @staticmethod
    def _contains_any(text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)
