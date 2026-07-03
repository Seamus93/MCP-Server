# Deployment

## Stato attuale

Il progetto espone una dashboard web FastAPI dockerizzata e un workflow GitHub Actions per CI, controlli di sicurezza e deploy VPS via SSH.

Durante il deploy la pipeline recupera i secret applicativi da Infisical e il VPS genera `.env` da `.env.example` tramite `scripts/render-env-file.sh`.

## Avvio locale web

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.web.app:app --reload
```

Dashboard:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Avvio locale MCP

```bash
python backend/server/main.py
```

## Docker locale

```bash
docker build -t mcp-server .
docker run --rm -p 8000:8000 mcp-server
```

## Docker Compose

```bash
docker compose up -d
```

## GitHub Actions

Workflow:

```text
.github/workflows/pipeline.yml
```

Pipeline:

1. installa dipendenze
2. esegue test
3. esegue controlli sicurezza
4. esegue Sonar se configurato
5. recupera secret runtime da Infisical
6. deploy VPS via `appleboy/ssh-action` se le credenziali SSH sono configurate
7. genera `.env` sul VPS e ricrea il container

## Secret richiesti per deploy VPS

```text
DEPLOY_HOST
DEPLOY_USER
DEPLOY_KEY
VPS_APP_DIR
INFISICAL_CLIENT_ID
INFISICAL_CLIENT_SECRET
```

`DEPLOY_KEY` deve essere una private key SSH completa e non protetta da passphrase.

Secret opzionali:

```text
PROJECT_URL
HEALTHCHECK_URL
MCP_GATEWAY_URL
MCP_GATEWAY_TOKEN
OPENAI_API_KEY
```

## VPS

Sul VPS servono:

```text
Docker
Docker Compose plugin
accesso SSH
```

La pipeline crea o usa:

```text
${VPS_APP_DIR:-/opt/projects/mcp-server}/docker-compose.yml
```

Il file `.env` sul VPS e rigenerato a ogni deploy quando `RENDER_DOTENV_FROM_ENV=true`.

## Reverse proxy consigliato

Caddy o Nginx davanti alla porta 8000.

## Integrazione MCP client

Esempio concettuale:

```text
mcp-server -> python /path/to/MCP-Server/backend/server/main.py
```

## Requisiti futuri

- HTTPS via reverse proxy
- autenticazione dashboard
- logging controllato
- sandbox comandi
- CI verde prima di release
