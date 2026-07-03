# Jarvis Core

## Obiettivo

Jarvis e il nucleo dell'AI Operating System personale. Riceve il task, delega la pianificazione al Planner, seleziona specialisti tramite Supervisor e Router, assegna MCP autorizzati e mantiene la responsabilita della risposta finale.

## Componenti

```text
jarvis/registry.py     agent registry, provider, modelli e MCP autorizzati
jarvis/router.py       selezione agente, provider, modello, MCP e tool
jarvis/supervisor.py   piano multi-agente con priorita, rischio e parallelismo
jarvis/formatter.py    formato risposta con metadati vocali
```

## Agenti iniziali

- Jarvis: supervisor executive
- Architect: architettura e strategia tecnica
- Coder: implementazione
- Reviewer: revisione qualita
- Security: sicurezza operativa
- DevOps: Docker, CI, VPS, SSH e deploy
- Analyst: analisi e classificazione
- Research: ricerca fonti e verifica
- Docs: documentazione
- Release: rilascio

## Pattern Supervisor

Flusso:

```text
Task utente
  -> Planner / Flight Plan
  -> Jarvis Supervisor
  -> Router modello/provider/MCP
  -> primary agent e specialisti
  -> Jarvis sintesi finale
  -> Google / Gateway
```

Esempio:

```text
"Implementa un endpoint sicuro"
  -> Coder
  -> Reviewer
  -> Security
  -> Jarvis summary
```

## Endpoint

```text
GET /api/jarvis/plan?task=...
GET /api/jarvis/flight-plan?task=...
GET /api/jarvis/capabilities
POST /api/voice-command
```

## MCP tool

```text
plan_supervised_task(task)
gemini_task(task, repository, repo_path)
```

## Risposta gateway

La risposta include prefisso agente primario:

```text
[Coder Agent | voce=forge | tono=diretto, operativo, pragmatico]
```

## Regola strategica

Gli specialisti producono analisi, patch, verifiche o report entro gli MCP autorizzati. Jarvis sintetizza in una risposta unica, breve e adatta a essere letta da Google.
