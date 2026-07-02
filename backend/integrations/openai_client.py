from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class ChatGPTResult:
    model: str
    output: str


class ChatGPTDelegate:
    """Small OpenAI wrapper used by the MCP tool layer.

    The API key is read from OPENAI_API_KEY.
    The model defaults to OPENAI_MODEL or gpt-4.1-mini.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, system_prompt: str, user_prompt: str) -> ChatGPTResult:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return ChatGPTResult(model=self.model, output=response.output_text)
