from __future__ import annotations

from dataclasses import asdict

from jarvis.registry import JarvisAgent, get_agent


KEYWORDS: dict[str, set[str]] = {
    "architect": {"architettura", "design", "struttura", "scalabil", "progetta", "roadmap"},
    "coder": {"implementa", "codice", "bug", "fix", "refactor", "endpoint", "parser", "test"},
    "reviewer": {"review", "controlla", "qualita", "regressione", "valida"},
    "security": {"sicurezza", "token", "segreto", "permessi", "auth", "oauth"},
    "docs": {"documenta", "readme", "docs", "guida", "manuale"},
    "release": {"release", "deploy", "versione", "changelog", "rilascio"},
}


class JarvisRouter:
    def select_agent(self, task: str) -> JarvisAgent:
        text = task.lower()
        for agent_key, keywords in KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return get_agent(agent_key)
        return get_agent("jarvis")

    def route_payload(self, task: str) -> dict[str, object]:
        agent = self.select_agent(task)
        return {
            "agent": asdict(agent),
            "speak_as": agent.voice,
            "tone": agent.tone,
            "model_policy": agent.model_policy,
            "task": task,
        }
