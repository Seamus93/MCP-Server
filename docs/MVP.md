# MVP - Gemini to ChatGPT via MCP

## Obiettivo

Consentire a Gemini, o a qualunque MCP client compatibile, di delegare un task tecnico a ChatGPT passando attraverso MCP-Server.

## Flusso MVP

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

### delegate_to_chatgpt

Delega il task a ChatGPT e restituisce una risposta operativa.

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

## Prossimo step

Aggiungere un tool `execute_plan` che applica patch solo dopo revisione esplicita.
