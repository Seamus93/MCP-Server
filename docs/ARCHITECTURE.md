# Architecture

## Scopo

Costruire Jarvis come AI Operating System personale: un Gateway unico riceve richieste, un Planner crea Flight Plan, il Supervisor orchestra agenti, il Router sceglie modelli e MCP, gli strumenti eseguono entro confini autorizzati.

## Flusso logico

```text
Google Home / Gemini / API / Dashboard
        ↓
Jarvis Gateway FastAPI
        ↓
Planner
        ↓
Supervisor
        ↓
Router
        ↓
Agenti specializzati
        ↓
MCP Tools
        ↓
Risultato unificato
```

## Componenti

- `backend/server/main.py`: espone i tool MCP.
- `backend/web/app.py`: espone la dashboard FastAPI e gli endpoint HTTP.
- `backend/jarvis/planner.py`: crea Flight Plan JSON senza eseguire.
- `backend/jarvis/supervisor.py`: decide agenti, sequenza, priorita, rischio e gruppi paralleli.
- `backend/jarvis/router.py`: sceglie agente, provider, modello, MCP e tool.
- `backend/jarvis/registry.py`: definisce agenti, personalita, modello preferito e MCP autorizzati.
- `backend/orchestrator/`: crea prompt pack e delega ai provider disponibili.
- `backend/prompts/`: istruzioni operative per agenti specializzati.
- `docs/`: memoria tecnica canonica del progetto.
- `.skills/`: registro skill locali e standard del repository.

## Principi

1. permessi minimi
2. tool piccoli e leggibili
3. niente shell arbitraria
4. ogni agente ha ruolo separato
5. ogni modifica importante aggiorna la documentazione
6. l'entrypoint web canonica e `backend.web.app:app`
7. l'utente non sceglie provider, modello o tool
8. ogni agente vede solo gli MCP autorizzati
