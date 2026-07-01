# Deployment

## Stato attuale

Il progetto espone una dashboard web FastAPI dockerizzata e un workflow GitHub Actions per build, push su GHCR e deploy opzionale su VPS.

## Avvio locale web

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn web.app:app --reload
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
python server/main.py
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
.github/workflows/docker-deploy.yml
```

Pipeline:

1. installa dipendenze
2. esegue test
3. build Docker
4. push immagine su GHCR
5. deploy VPS via SSH se i secret sono configurati

## Secret richiesti per deploy VPS

```text
VPS_HOST
VPS_USER
VPS_SSH_KEY
VPS_PORT opzionale
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
~/mcp-server/docker-compose.yml
```

## Reverse proxy consigliato

Caddy o Nginx davanti alla porta 8000.

## Integrazione MCP client

Esempio concettuale:

```text
mcp-server -> python /path/to/MCP-Server/server/main.py
```

## Requisiti futuri

- HTTPS via reverse proxy
- autenticazione dashboard
- logging controllato
- sandbox comandi
- CI verde prima di release
