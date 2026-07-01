# MVP - Gemini to ChatGPT via MCP

## Obiettivo

Consentire a Gemini, o a qualunque MCP client compatibile, di delegare un task tecnico a ChatGPT passando attraverso MCP-Server.

## Flusso zero-cost

```text
Utente parla con Gemini
        ↓
Gemini chiama tool MCP
        ↓
create_chatgpt_prompt_pack(task, repository, repo_path)
        ↓
MCP genera un prompt pack in .mcp_outbox
        ↓
Utente incolla il prompt in ChatGPT Pro
        ↓
Utente incolla la risposta in ingest_chatgpt_response
        ↓
MCP salva un piano strutturato in .mcp_outbox/responses
```

## Flusso API futuro

```text
Utente parla con Gemini
        ↓
Gemini chiama tool MCP
        ↓
delegate_to_chatgpt(task, repository, repo_path)
        ↓
TaskRouter seleziona agenti
        ↓
DelegationExecutor costruisce contesto
        ↓
ChatGPT produce piano operativo
        ↓
Gemini legge il risultato
```

## Tool esposti

### route_task

Simula il routing agentico senza chiamare OpenAI.

### create_chatgpt_prompt_pack

Genera un prompt pack locale da incollare manualmente in ChatGPT Pro.

Non richiede API key.

### ingest_chatgpt_response

Prende la risposta manuale di ChatGPT, estrae sezioni operative, valida il formato e salva un artefatto JSON.

Stati possibili:

- `planned`: risposta strutturata e utilizzabile
- `needs_review`: mancano sezioni o ci sono warning

### delegate_to_chatgpt

Delega il task a ChatGPT tramite OpenAI API.

Richiede:

```text
OPENAI_API_KEY
```

Opzionale:

```text
OPENAI_MODEL
```

## Limiti intenzionali

- non modifica ancora file automaticamente
- non fa commit/push
- non apre PR
- produce piani e analisi operative
- nel flusso zero-cost serve copia/incolla manuale

## Prossimo step

Aggiungere `approve_plan` ed `execute_plan` per applicare patch solo dopo approvazione esplicita.
