from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateStore:
    def __init__(self, folder: str = ".mcp_outbox/responses") -> None:
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def read(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path).resolve()
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, file_path: str, payload: dict[str, Any]) -> str:
        path = Path(file_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)

    def update_status(self, file_path: str, status: str) -> str:
        payload = self.read(file_path)
        payload["status"] = status
        return self.write(file_path, payload)

    def list_items(self) -> list[dict[str, str]]:
        items = []
        for path in sorted(self.folder.glob("*.json"), reverse=True):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                payload = {"status": "invalid", "summary": "invalid json"}
            items.append({"path": str(path), "status": str(payload.get("status", "unknown")), "summary": str(payload.get("summary", ""))[:160]})
        return items
