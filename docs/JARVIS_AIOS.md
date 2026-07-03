# Jarvis AI Operating System

## Visione

Jarvis e il supervisore unico del progetto. Riceve richieste da API, dashboard, voce, Google Home, Gemini o altri webhook, crea un piano, sceglie gli agenti migliori, assegna MCP e tool autorizzati, coordina l'esecuzione e restituisce una risposta unica.

L'utente non sceglie modello, provider o tool. Jarvis decide in base al task, al rischio e al canale di ingresso.

## Flusso target

```text
Utente
  -> Google Home / Gemini / API / Dashboard
  -> Jarvis Gateway FastAPI
  -> Planner
  -> Supervisor
  -> Router
  -> Agenti specializzati
  -> MCP Tools
  -> Risultato unificato
```

## Ruoli interni

- Planner: comprende il problema e genera un Flight Plan. Non esegue.
- Supervisor: riceve il Flight Plan, decide agenti, ordine, parallelismo, priorita e rischio.
- Router: seleziona provider, modello, MCP e tool per ogni agente.
- Agenti: eseguono lavoro specialistico entro i confini autorizzati.
- MCP: espongono risorse e servizi in modo controllato.
- Gateway: espone API REST, dashboard, voce, Google Home, IFTTT e Gemini.

## Agenti canonici

- Jarvis: supervisore AIOS e sintesi finale.
- Architect: architettura e strategia tecnica.
- Coder: implementazione.
- Reviewer: qualita, regressioni e mantenibilita.
- Security: permessi, path, segreti e rischio operativo.
- DevOps: Docker, CI, VPS, SSH, deploy e rollback.
- Analyst: analisi, classificazione e report.
- Research: ricerca fonti e verifica esterna.
- Docs: documentazione canonica.
- Release: changelog, checklist e note operative.

## MCP autorizzati per agente

Ogni agente vede solo gli MCP dichiarati nel registry. La selezione corrente e in `backend/jarvis/registry.py`.

Esempi:

- Coder: filesystem, git, terminal, tests.
- DevOps: git, docker, terminal, ssh, github.
- Security: filesystem, git, secrets, audit.
- Research: browser, github, google-drive.
- Docs: filesystem, docs, google-drive.

## Multi-modello

Jarvis non dipende da un singolo provider. Il Router puo indirizzare verso OpenRouter, Gemini, Claude, OpenAI, DeepSeek, Qwen, Mistral, Grok o altri provider configurabili.

Le policy correnti sono metadati operativi. L'esecuzione reale dei provider verra collegata progressivamente tramite integrazioni dedicate.

## Stato attuale

Il progetto implementa il kernel deterministico dell'AIOS:

- registry agenti con provider, modello e MCP autorizzati
- Router con decisione provider/modello/MCP/tool
- Supervisor con priorita, rischio e gruppi di parallelizzazione
- Flight Planner JSON
- Gateway FastAPI canonico `backend.web.app:app`
- Dashboard per task, workflow e capability agentiche

## Stato target

Il completamento richiede:

- integrazioni provider reali dietro le policy del Router
- MCP Docker, SSH, Browser, GitHub, Google Drive, Calendar ed Email
- memoria persistente di workflow e preferenze
- audit log e policy di sicurezza per ogni tool
- endpoint Google Home/IFTTT/Gemini pronti per produzione
- esecuzione controllata dei Flight Plan con rollback e report finale
