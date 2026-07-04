from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositoryEntry:
    key: str
    name: str
    github: str
    local_path: str
    description: str = ""


class RepositoryRegistry:
    def __init__(self, config_path: str = "config/repositories.json") -> None:
        self.config_path = Path(config_path)

    def load_all(self) -> dict[str, RepositoryEntry]:
        if not self.config_path.exists():
            return {}
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        entries: dict[str, RepositoryEntry] = {}
        for key, value in data.get("repositories", {}).items():
            entries[key.lower()] = RepositoryEntry(
                key=key.lower(),
                name=str(value.get("name", key)),
                github=str(value.get("github", "")),
                local_path=str(value.get("local_path", "")),
                description=str(value.get("description", "")),
            )
        return entries

    def resolve(self, query: str) -> RepositoryEntry | None:
        normalized = query.lower().strip()
        entries = self.load_all()
        if normalized in entries:
            return entries[normalized]
        for entry in entries.values():
            values = [entry.name.lower(), entry.github.lower(), entry.description.lower()]
            if any(normalized in value for value in values):
                return entry
        return None

    def list_entries(self) -> list[RepositoryEntry]:
        return list(self.load_all().values())
