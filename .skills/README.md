# MCP-Server

MCP server sperimentale per orchestrare agenti specializzati su repository GitHub.

Obiettivo: usare un assistente vocale come front-end e delegare a tool MCP operazioni controllate su codice, test, documentazione e workflow.

## Architettura

```text
Voice Assistant / ChatGPT / IDE Agent
        ↓
MCP Client
        ↓
MCP-Server
        ↓
GitHub / filesystem / test runner / orchestrator
```

## Setup locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server/main.py
```

## Tool iniziali

- `health_check` — verifica che il server risponda.
- `git_status` — legge lo stato Git di un repository locale.
- `list_files` — lista file in modo controllato.
- `read_text_file` — legge file testuali con limite caratteri.
- `run_python_tests` — esegue pytest in un repository locale.

## Regola sicurezza

Niente comandi arbitrari. Ogni tool deve essere chiuso, leggibile e con permessi minimi.

## Roadmap

- Agent Architect
- Agent Coder
- Agent Reviewer
- Agent Security
- Agent Release
- integrazione GitHub PR/issues
- workflow CI
