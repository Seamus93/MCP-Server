from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpeechOutputRequest:
    text: str
    target_path: str
    voice: str = "default"


class SpeechOutput:
    """Base interface for text to audio providers."""

    def create_audio(self, request: SpeechOutputRequest) -> str:
        target = Path(request.target_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(request.text, encoding="utf-8")
        return str(target)
