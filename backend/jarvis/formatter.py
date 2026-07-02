from __future__ import annotations

from jarvis.registry import JarvisAgent


def format_agent_response(agent: JarvisAgent, body: str) -> str:
    return (
        f"[{agent.name} | voce={agent.voice} | tono={agent.tone}]\n\n"
        f"{body}\n\n"
        f"Model policy: {agent.model_policy}"
    )


def format_gateway_intro(agent: JarvisAgent) -> str:
    return f"Parla {agent.name}. Tono: {agent.tone}."
