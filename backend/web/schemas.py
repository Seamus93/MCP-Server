from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceCommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    repository: str | None = "Seamus93/MCP-Server"
    repo_path: str | None = None
    risk_level: str = "normal"
    mode: str = "prompt_pack"


class VoiceCommandResponse(BaseModel):
    status: str
    mode: str
    reply: str
    next_step: str
