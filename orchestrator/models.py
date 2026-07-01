from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AgentRole(str, Enum):
    ARCHITECT = "architect"
    CODER = "coder"
    REVIEWER = "reviewer"
    SECURITY = "security"
    RELEASE = "release"
    DOCS = "docs"


@dataclass(frozen=True)
class AgentSpec:
    role: AgentRole
    name: str
    mission: str
    prompt_path: str
    can_write_code: bool = False
    can_release: bool = False


@dataclass
class TaskRequest:
    title: str
    description: str
    repository: str | None = None
    files_hint: list[str] = field(default_factory=list)
    risk_level: str = "normal"


@dataclass
class RoutedTask:
    request: TaskRequest
    agents: list[AgentSpec]
    execution_notes: list[str]
