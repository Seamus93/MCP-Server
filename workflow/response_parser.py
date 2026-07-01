from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ParsedChatGPTResponse:
    status: str
    summary: str = ""
    plan: str = ""
    files_to_modify: list[str] = field(default_factory=list)
    patch: str = ""
    tests: str = ""
    risks: str = ""
    next_action: str = ""
    raw_response: str = ""
    warnings: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


SECTION_ALIASES = {
    "sintesi": "summary",
    "piano operativo": "plan",
    "piano": "plan",
    "file da modificare": "files_to_modify",
    "file modificati": "files_to_modify",
    "patch proposta": "patch",
    "patch": "patch",
    "test consigliati": "tests",
    "test": "tests",
    "rischi": "risks",
    "prossima azione": "next_action",
    "next action": "next_action",
}


class ChatGPTResponseParser:
    """Parse a manual ChatGPT response into a structured workflow artifact."""

    def parse(self, response: str) -> ParsedChatGPTResponse:
        sections = self._extract_sections(response)
        parsed = ParsedChatGPTResponse(
            status="planned",
            summary=sections.get("summary", "").strip(),
            plan=sections.get("plan", "").strip(),
            files_to_modify=self._extract_files(sections.get("files_to_modify", "")),
            patch=sections.get("patch", "").strip(),
            tests=sections.get("tests", "").strip(),
            risks=sections.get("risks", "").strip(),
            next_action=sections.get("next_action", "").strip(),
            raw_response=response,
        )
        parsed.warnings = self._validate(parsed)
        if parsed.warnings:
            parsed.status = "needs_review"
        return parsed

    def save(
        self,
        parsed: ParsedChatGPTResponse,
        outbox_dir: str = ".mcp_outbox/responses",
        response_id: str | None = None,
    ) -> str:
        target_dir = Path(outbox_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        file_id = response_id or f"response-{timestamp}"
        path = target_dir / f"{file_id}.json"
        path.write_text(parsed.to_json(), encoding="utf-8")
        return str(path)

    def _extract_sections(self, response: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        matches = list(
            re.finditer(
                r"(?im)^\s*(?:#{1,3}\s*)?(?:\d+[.)]\s*)?([A-Za-zÀ-ÿ ]{3,40})\s*:?") ,
                response,
            )
        )

        for index, match in enumerate(matches):
            title = match.group(1).strip().lower()
            key = SECTION_ALIASES.get(title)
            if not key:
                continue
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(response)
            sections[key] = response[start:end].strip()

        if not sections:
            sections["summary"] = response.strip()
        return sections

    @staticmethod
    def _extract_files(text: str) -> list[str]:
        if not text.strip():
            return []
        files: list[str] = []
        for line in text.splitlines():
            cleaned = line.strip().lstrip("-*").strip().strip("`")
            if cleaned and ("/" in cleaned or "." in cleaned):
                files.append(cleaned)
        return files

    @staticmethod
    def _validate(parsed: ParsedChatGPTResponse) -> list[str]:
        warnings: list[str] = []
        if not parsed.summary:
            warnings.append("missing_summary")
        if not parsed.plan:
            warnings.append("missing_plan")
        if not parsed.next_action:
            warnings.append("missing_next_action")
        if parsed.patch and not parsed.files_to_modify:
            warnings.append("patch_without_files")
        return warnings
