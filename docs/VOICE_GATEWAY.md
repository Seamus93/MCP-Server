# Voice Gateway

## Obiettivo

Esporre un endpoint HTTP semplice che puo essere chiamato da Google Assistant, IFTTT, Tasker, Automate, una futura APK o qualunque webhook.

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
  "command": "Lavora su AsteSmart e proponi il prossimo step",
  "repository": "Seamus93/Astesmart",
  "repo_path": "/home/ubuntu/repos/Astesmart",
  "risk_level": "normal",
  "mode": "prompt_pack"
}
```

## Modalita

### prompt_pack

Modalita zero-cost. Genera un prompt pack da incollare in ChatGPT Pro.

### api

Modalita futura. Usa OpenAI API tramite `delegate_task`.

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

1. Comando vocale a Google Assistant che attiva una routine o Tasker.
2. Tasker invia POST a `/api/voice-command`.
3. Il VPS genera il prompt pack.
4. L'utente incolla il prompt in ChatGPT Pro.
5. La risposta viene acquisita tramite `/api/ingest-response`.
