from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class NotesStore:
    def __init__(self, folder: str = ".mcp_outbox/notes") -> None:
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def add(self, title: str, body: str, tags: list[str] | None = None) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.folder / f"{timestamp}.json"
        payload = {"title": title, "body": body, "tags": tags or [], "created_at": timestamp}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)

    def search(self, query: str, limit: int = 10) -> list[dict[str, str]]:
        results: list[dict[str, str]] = []
        q = query.lower().strip()
        for path in sorted(self.folder.glob("*.json"), reverse=True):
            data = json.loads(path.read_text(encoding="utf-8"))
            haystack = f"{data.get('title', '')} {data.get('body', '')} {' '.join(data.get('tags', []))}".lower()
            if q in haystack:
                results.append({"path": str(path), "title": str(data.get("title", "")), "body": str(data.get("body", ""))[:300]})
            if len(results) >= limit:
                break
        return results
