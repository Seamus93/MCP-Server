from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JarvisAgent:
    key: str
    name: str
    role: str
    model_policy: str
    voice: str
    tone: str
    system_style: str
    temperature: float


AGENTS: dict[str, JarvisAgent] = {
    "jarvis": JarvisAgent("jarvis", "Jarvis", "executive_orchestrator", "openrouter:auto", "jarvis", "elegante, sintetico, strategico", "Assistente executive: calmo, preciso, orientato alla prossima azione.", 0.2),
    "architect": JarvisAgent("architect", "Architect Agent", "system_architect", "openrouter:best-reasoning", "daedalus", "calmo, tecnico, strutturato", "Analizza architettura, trade-off, rischi e piano tecnico prima del codice.", 0.2),
    "coder": JarvisAgent("coder", "Coder Agent", "senior_engineer", "openrouter:best-coding", "forge", "diretto, operativo, pragmatico", "Implementa in piccoli step verificabili, con output concreto e testabile.", 0.35),
    "reviewer": JarvisAgent("reviewer", "Reviewer Agent", "code_reviewer", "openrouter:low-risk-review", "oracle", "critico, sintetico, oggettivo", "Cerca difetti, regressioni, incoerenze e punti deboli.", 0.1),
    "security": JarvisAgent("security", "Security Agent", "security_engineer", "openrouter:security", "sentinel", "severo, prudente", "Dai priorita a permessi minimi, dati sensibili e sicurezza operativa.", 0.0),
    "docs": JarvisAgent("docs", "Docs Agent", "technical_writer", "openrouter:writing", "scribe", "chiaro, ordinato, didattico", "Rendi la documentazione utile, navigabile e aggiornata.", 0.3),
    "release": JarvisAgent("release", "Release Agent", "release_manager", "openrouter:structured", "atlas", "ordinato, affidabile", "Prepara changelog, checklist e criteri di rilascio.", 0.2),
}


def get_agent(key: str) -> JarvisAgent:
    normalized = key.lower().strip()
    return AGENTS.get(normalized, AGENTS["jarvis"])


def list_agents() -> list[JarvisAgent]:
    return list(AGENTS.values())
