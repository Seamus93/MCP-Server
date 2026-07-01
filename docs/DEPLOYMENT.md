# Deployment

## Stato attuale

Non esiste ancora un deploy production.

## Avvio locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server/main.py
```

## Integrazione MCP client

Esempio concettuale:

```text
mcp-server -> python /path/to/MCP-Server/server/main.py
```

## Requisiti futuri

- variabili sensibili fuori dal repo
- logging controllato
- sandbox comandi
- CI verde prima di release
