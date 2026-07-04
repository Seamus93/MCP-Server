from __future__ import annotations

from dataclasses import dataclass

from registry.repository_registry import RepositoryRegistry
from workflow.intent_router import IntentRouter


@dataclass(frozen=True)
class TaskPlan:
    text: str
    kind: str
    repository: str | None
    repo_path: str | None
    next_action: str


class TaskPlanner:
    def __init__(self, registry: RepositoryRegistry | None = None) -> None:
        self.registry = registry or RepositoryRegistry()
        self.router = IntentRouter()

    def plan(self, text: str) -> TaskPlan:
        intent = self.router.classify(text)
        repository = None
        repo_path = None
        if intent.repository_hint:
            entry = self.registry.resolve(intent.repository_hint)
            if entry:
                repository = entry.github
                repo_path = entry.local_path
        next_action = "create_prompt_pack" if intent.intent == "repository_task" else "respond"
        return TaskPlan(text=text, kind=intent.intent, repository=repository, repo_path=repo_path, next_action=next_action)
