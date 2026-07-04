from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntentResult:
    intent: str
    confidence: float
    repository_hint: str | None = None


class IntentRouter:
    def classify(self, text: str) -> IntentResult:
        value = text.lower()
        repo_hint = self._extract_repo_hint(value)
        if any(word in value for word in ["repo", "repository", "astesmart", "agri", "mcp"]):
            return IntentResult(intent="repository_task", confidence=0.85, repository_hint=repo_hint)
        if any(word in value for word in ["note", "ricorda", "salva"]):
            return IntentResult(intent="note", confidence=0.75, repository_hint=repo_hint)
        if any(word in value for word in ["pagina", "sito", "url"]):
            return IntentResult(intent="web_read", confidence=0.7, repository_hint=repo_hint)
        return IntentResult(intent="general", confidence=0.5, repository_hint=repo_hint)

    @staticmethod
    def _extract_repo_hint(value: str) -> str | None:
        known = ["astesmart", "agriavenger", "agri", "mcp-server", "mcp"]
        for item in known:
            if item in value:
                return item
        return None
