# Jarvis Core

## Obiettivo

Jarvis non e piu un semplice router keyword-based. Ora usa un pattern Supervisor: Jarvis riceve il task, seleziona uno o piu specialisti, impone una sequenza di lavoro e mantiene la responsabilita della risposta finale.

## Componenti

```text
jarvis/registry.py     agent registry
jarvis/router.py       selezione primary agent
jarvis/supervisor.py   piano multi-agente supervisionato
jarvis/formatter.py    formato risposta con metadati vocali
```

## Agenti iniziali

- Jarvis: supervisor executive
- Architect: architettura e strategia tecnica
- Coder: implementazione
- Reviewer: revisione qualita
- Security: sicurezza operativa
- Docs: documentazione
- Release: rilascio

## Pattern Supervisor

Flusso:

```text
Task utente
  -> Jarvis Supervisor
  -> primary agent
  -> specialisti aggiuntivi se necessari
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

Gli specialisti producono analisi e piano. Jarvis sintetizza in una risposta unica, breve e adatta a essere letta da Google.
