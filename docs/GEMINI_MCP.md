# Gemini MCP Workflow

## Obiettivo

Permettere a Gemini, quando configurato come MCP client, di invocare il server locale e ricevere una risposta operativa.

## Tool principale

```text
gemini_task
```

Input consigliato:

```text
task: richiesta in linguaggio naturale
repository: owner/repo
repo_path: path locale del repository, se disponibile
risk_level: normal oppure high
```

## Flusso zero-cost

1. Gemini chiama `gemini_task`.
2. MCP genera un prompt pack in `.mcp_outbox`.
3. Gemini riceve il testo del prompt pack come risposta MCP.
4. L'operatore incolla il prompt in ChatGPT Pro.
5. L'operatore incolla la risposta in `ingest_chatgpt_response`.
6. MCP salva un artefatto JSON in `.mcp_outbox/responses`.
7. L'operatore usa `approve_plan` se il piano e valido.
8. L'operatore usa `verify_plan_diff` se la risposta contiene patch.

## Stato MVP

Il sistema e pronto per:

- ricevere comandi da un client MCP
- generare prompt pack compatibili con ChatGPT Pro
- caricare standard progetto da `.skills`, `AGENTS.md` e `docs/`
- acquisire risposte manuali
- validare e tracciare piani

## Limite attuale

Gemini deve supportare o essere collegato a un MCP client capace di lanciare questo server locale.
