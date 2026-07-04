from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AudioInputResult:
    text: str
    source_path: str
    provider: str


class AudioInput:
    """Base interface for audio input providers."""

    def read_text_source(self, path: str) -> AudioInputResult:
        source = Path(path).resolve()
        text = source.read_text(encoding="utf-8", errors="replace")
        return AudioInputResult(text=text.strip(), source_path=str(source), provider="text-file")
