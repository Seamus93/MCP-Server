from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ManualPromptPack:
    id: str
    path: str
    content: str


class ManualProvider:
    """Zero-cost provider.

    It creates a prompt pack that the user can paste into ChatGPT Pro manually.
    This keeps the MVP independent from paid APIs and avoids brittle browser automation.
    """

    def __init__(self, outbox_dir: str = ".mcp_outbox") -> None:
        self.outbox_dir = Path(outbox_dir)

    def create_prompt_pack(
        self,
        task: str,
        system_prompt: str,
        context: str,
        repository: str | None = None,
    ) -> ManualPromptPack:
        self.outbox_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        pack_id = f"manual-{timestamp}"
        content = self._render_prompt(
            task=task,
            system_prompt=system_prompt,
            context=context,
            repository=repository,
            pack_id=pack_id,
        )
        path = self.outbox_dir / f"{pack_id}.md"
        path.write_text(content, encoding="utf-8")
        return ManualPromptPack(id=pack_id, path=str(path), content=content)

    @staticmethod
    def _render_prompt(
        task: str,
        system_prompt: str,
        context: str,
        repository: str | None,
        pack_id: str,
    ) -> str:
        return f"""# Manual ChatGPT Prompt Pack

ID: {pack_id}
Repository: {repository or "non specificato"}

## Istruzioni sistema

{system_prompt}

## Task

{task}

## Contesto

{context}

## Output richiesto

Rispondi con queste sezioni:

1. Sintesi
2. Piano operativo
3. File da modificare
4. Patch proposta, se possibile
5. Test consigliati
6. Rischi
7. Prossima azione
""".strip()
