from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JarvisAgent:
    key: str
    name: str
    role: str
    preferred_provider: str
    preferred_model: str
    model_policy: str
    voice: str
    tone: str
    system_style: str
    temperature: float
    allowed_mcps: tuple[str, ...]


AGENTS: dict[str, JarvisAgent] = {
    "jarvis": JarvisAgent("jarvis", "Jarvis", "aios_supervisor", "openrouter", "auto", "openrouter:auto", "jarvis", "elegante, sintetico, strategico", "Supervisore unico: comprende la richiesta, orchestra agenti e restituisce una risposta unificata.", 0.2, ("memory", "workflow", "gateway")),
    "architect": JarvisAgent("architect", "Architect Agent", "system_architect", "openrouter", "best-reasoning", "openrouter:best-reasoning", "daedalus", "calmo, tecnico, strutturato", "Analizza architettura, trade-off, rischi e piano tecnico prima del codice.", 0.2, ("filesystem", "git", "github", "docs")),
    "coder": JarvisAgent("coder", "Coder Agent", "senior_engineer", "claude", "best-coding", "claude:best-coding", "forge", "diretto, operativo, pragmatico", "Implementa in piccoli step verificabili, con output concreto e testabile.", 0.35, ("filesystem", "git", "terminal", "tests")),
    "reviewer": JarvisAgent("reviewer", "Reviewer Agent", "code_reviewer", "openai", "review", "openai:low-risk-review", "oracle", "critico, sintetico, oggettivo", "Cerca difetti, regressioni, incoerenze e punti deboli.", 0.1, ("filesystem", "git", "tests")),
    "security": JarvisAgent("security", "Security Agent", "security_engineer", "openrouter", "security", "openrouter:security", "sentinel", "severo, prudente", "Dai priorita a permessi minimi, dati sensibili e sicurezza operativa.", 0.0, ("filesystem", "git", "secrets", "audit")),
    "devops": JarvisAgent("devops", "DevOps Agent", "deployment_engineer", "openai", "ops-structured", "openai:ops-structured", "atlas", "operativo, prudente", "Verifica build, container, pipeline, deploy e rollback.", 0.15, ("git", "docker", "terminal", "ssh", "github")),
    "analyst": JarvisAgent("analyst", "Analyst Agent", "systems_analyst", "gemini", "flash", "gemini:flash", "lens", "rapido, ordinato", "Classifica richieste, estrae segnali e produce sintesi operative.", 0.25, ("memory", "filesystem", "workflow")),
    "research": JarvisAgent("research", "Research Agent", "research_specialist", "perplexity", "research", "perplexity:research", "compass", "curioso, verificabile", "Cerca fonti, confronta informazioni e segnala incertezze.", 0.2, ("browser", "github", "google-drive")),
    "docs": JarvisAgent("docs", "Docs Agent", "technical_writer", "mistral", "writing", "mistral:writing", "scribe", "chiaro, ordinato, didattico", "Rendi la documentazione utile, navigabile e aggiornata.", 0.3, ("filesystem", "docs", "google-drive")),
    "release": JarvisAgent("release", "Release Agent", "release_manager", "openrouter", "structured", "openrouter:structured", "atlas", "ordinato, affidabile", "Prepara changelog, checklist e criteri di rilascio.", 0.2, ("git", "github", "docker", "docs")),
}


def get_agent(key: str) -> JarvisAgent:
    normalized = key.lower().strip()
    return AGENTS.get(normalized, AGENTS["jarvis"])


def list_agents() -> list[JarvisAgent]:
    return list(AGENTS.values())
