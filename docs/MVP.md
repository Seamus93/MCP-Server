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
Utente riporta la risposta nel workflow
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

Aggiungere un tool `ingest_chatgpt_response` che prende la risposta manuale e la trasforma in piano verificabile.
