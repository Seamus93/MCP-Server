# Voice Gateway

## Obiettivo

Esporre il Jarvis Gateway HTTP per Google Assistant/Home, IFTTT, Tasker, Automate, Gemini, una futura APK o qualunque webhook.

## Endpoint principale

```text
POST /api/voice-command
```

Header consigliato:

```text
Authorization: Bearer <MCP_GATEWAY_TOKEN>
```

Body:

```json
{
  "command": "Lavora su mcp-server e proponi il prossimo step",
  "repository": "Seamus93/mcp-server",
  "repo_path": "/home/ubuntu/repos/mcp-server",
  "risk_level": "normal",
  "mode": "prompt_pack"
}
```

## Modalita

### prompt_pack

Modalita zero-cost. Genera un prompt pack da incollare in ChatGPT Pro.

### api

Usa il provider configurato dietro `delegate_task`. Il Router resta responsabile della scelta di modello e tool.

## Capability Jarvis

```text
GET /api/jarvis/capabilities
```

Restituisce agenti, provider preferiti, modelli e MCP autorizzati.

## Ingest risposta ChatGPT

```text
POST /api/ingest-response
```

Parametri:

```text
response=<testo risposta ChatGPT>
response_id=<opzionale>
```

## Lista workflow

```text
GET /api/workflows
```

## Sicurezza

Impostare nel VPS:

```bash
export MCP_GATEWAY_TOKEN="token-lungo-random"
```

Se il token non e configurato, gli endpoint restano aperti. Da non fare quando il servizio sara esposto online.

## Uso con Android

Soluzioni compatibili:

- Tasker HTTP Request
- Automate HTTP request block
- IFTTT Webhooks
- futura APK minimale
- browser web dashboard

## Flusso consigliato Android iniziale

1. Comando vocale a Google Home o Google Assistant.
2. Routine, IFTTT o Tasker invia POST a `/api/voice-command`.
3. Jarvis Gateway crea piano, routing e prompt pack o esecuzione API.
4. Gli agenti lavorano tramite MCP autorizzati.
5. Jarvis restituisce una risposta unica.
6. Google legge la risposta.
