# VPS Pull Deploy

## Obiettivo

Rendere il VPS aggiornabile con un solo pull/script.

## Prima installazione

```bash
git clone https://github.com/Seamus93/MCP-Server.git ~/mcp-server
cd ~/mcp-server
bash scripts/bootstrap_vps.sh
```

## Avvio manuale web

```bash
bash scripts/run_web.sh
```

## Avvio manuale MCP stdio

```bash
bash scripts/run_mcp.sh
```

## Aggiornamento dopo modifiche GitHub

```bash
cd ~/mcp-server
bash scripts/update_vps.sh
```

Lo script fa:

1. `git pull --ff-only`
2. crea `.venv` se manca
3. aggiorna dipendenze
4. esegue test
5. riavvia `mcp-server.service` se installato

## Installazione servizio systemd

```bash
cd ~/mcp-server
bash scripts/install_systemd.sh
```

Dopo questa operazione:

```bash
sudo systemctl status mcp-server
sudo systemctl restart mcp-server
```

## Flusso ideale

```bash
cd ~/mcp-server
bash scripts/update_vps.sh
```

## Note

- DuckDNS e reverse proxy verranno aggiunti dopo.
- Il servizio web ascolta su porta `8000`.
- Gli artefatti locali restano in `.mcp_outbox/`.
