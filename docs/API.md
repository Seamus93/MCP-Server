# API

## Tool MCP correnti

### health_check

Verifica che il server MCP sia online.

### git_status

Input: `repo_path`

Restituisce `git status --short` del repository locale.

### list_files

Input: `root_path`, `max_files`

Lista file ignorando cartelle generate o pesanti.

### read_text_file

Input: `path`, `max_chars`

Legge file UTF-8 con limite caratteri.

### run_python_tests

Input: `repo_path`

Esegue `python -m pytest -q` con timeout.

### plan_supervised_task

Input: `task`

Restituisce il piano Supervisor con agenti, provider, modello, MCP autorizzati, priorita e rischio.

### create_flight_plan

Input: `task`, `repository`, `repo_path`

Restituisce il Flight Plan JSON creato dal Planner.

### gemini_task

Input: `task`, `repository`, `repo_path`, `risk_level`, `outbox_dir`

Crea il prompt pack Jarvis per il flusso Gemini/MCP/ChatGPT Pro manuale.

## Endpoint HTTP Jarvis Gateway

```text
GET /api/jarvis/plan?task=...
GET /api/jarvis/flight-plan?task=...
GET /api/jarvis/capabilities
POST /api/voice-command
POST /api/ingest-response
GET /api/workflows
```
