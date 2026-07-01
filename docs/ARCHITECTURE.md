# Architecture

## Scopo

Separare interfaccia conversazionale, orchestrazione e tool eseguibili.

## Flusso logico

```text
Voice Assistant / ChatGPT / IDE Agent
        ↓
MCP Client
        ↓
MCP-Server
        ↓
Tool sicuri + Orchestrator
        ↓
Repository / test runner / documentazione
```

## Componenti

- `server/main.py`: espone i tool MCP.
- `orchestrator/`: modelli, registry agenti e routing task.
- `prompts/`: istruzioni operative per agenti specializzati.
- `docs/`: memoria tecnica canonica del progetto.
- `.skills/`: registro skill locali e standard del repository.

## Principi

1. permessi minimi
2. tool piccoli e leggibili
3. niente shell arbitraria
4. ogni agente ha ruolo separato
5. ogni modifica importante aggiorna la documentazione
