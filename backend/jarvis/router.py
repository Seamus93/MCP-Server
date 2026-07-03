from __future__ import annotations

from dataclasses import asdict, dataclass

from backend.jarvis.registry import JarvisAgent, get_agent


KEYWORDS: dict[str, set[str]] = {
    "security": {"sicurezza", "token", "segreto", "permessi", "auth", "oauth"},
    "devops": {"deploy", "docker", "container", "pipeline", "ci", "vps", "ssh", "rollback"},
    "architect": {"architettura", "design", "struttura", "scalabil", "progetta", "roadmap"},
    "coder": {"implementa", "codice", "bug", "fix", "refactor", "endpoint", "parser", "test"},
    "reviewer": {"review", "controlla", "qualita", "regressione", "valida"},
    "analyst": {"analizza", "classifica", "sintetizza", "metriche", "report"},
    "research": {"ricerca", "fonti", "browser", "web", "latest", "aggiornato"},
    "docs": {"documenta", "readme", "docs", "guida", "manuale"},
    "release": {"release", "versione", "changelog", "rilascio"},
}


@dataclass(frozen=True)
class RouteDecision:
    agent: JarvisAgent
    provider: str
    model: str
    model_policy: str
    mcps: tuple[str, ...]
    tools: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "agent": asdict(self.agent),
            "provider": self.provider,
            "model": self.model,
            "model_policy": self.model_policy,
            "mcps": list(self.mcps),
            "tools": list(self.tools),
            "speak_as": self.agent.voice,
            "tone": self.agent.tone,
        }


class JarvisRouter:
    def select_agent(self, task: str) -> JarvisAgent:
        text = task.lower()
        for agent_key, keywords in KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return get_agent(agent_key)
        return get_agent("jarvis")

    def route(self, task: str) -> RouteDecision:
        agent = self.select_agent(task)
        return self.route_agent(agent)

    def route_agent(self, agent: JarvisAgent) -> RouteDecision:
        return RouteDecision(
            agent=agent,
            provider=agent.preferred_provider,
            model=agent.preferred_model,
            model_policy=agent.model_policy,
            mcps=agent.allowed_mcps,
            tools=self._tools_for(agent),
        )

    def route_payload(self, task: str) -> dict[str, object]:
        payload = self.route(task).to_dict()
        payload["task"] = task
        return payload

    @staticmethod
    def _tools_for(agent: JarvisAgent) -> tuple[str, ...]:
        tool_map = {
            "filesystem": ("read_file", "list_files"),
            "git": ("git_status", "git_diff"),
            "terminal": ("run_tests",),
            "docker": ("docker_build", "docker_logs"),
            "ssh": ("deploy_vps",),
            "github": ("issues", "pull_requests"),
            "browser": ("web_search",),
            "google-drive": ("drive_search", "docs_read"),
            "docs": ("update_docs",),
            "tests": ("pytest",),
            "secrets": ("secret_audit",),
            "audit": ("permission_audit",),
            "memory": ("workflow_state",),
            "workflow": ("flight_plan",),
            "gateway": ("voice_command",),
        }
        tools: list[str] = []
        for mcp in agent.allowed_mcps:
            tools.extend(tool_map.get(mcp, ()))
        return tuple(dict.fromkeys(tools))
