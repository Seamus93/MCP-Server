from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageSnapshot:
    source: str
    text: str


class PageSnapshotReader:
    def read_text_file(self, path: str, max_chars: int = 4000) -> PageSnapshot:
        source = Path(path).resolve()
        content = source.read_text(encoding="utf-8", errors="replace")[:max_chars]
        return PageSnapshot(source=str(source), text=content)
