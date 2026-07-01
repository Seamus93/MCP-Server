# PM Status

## Stato

MVP core completato per workflow Gemini to MCP to ChatGPT Pro manuale.

## Ultimo avanzamento

- aggiunto tool `gemini_task` come comando principale per Gemini
- aggiunto caricamento standard progetto da `.skills`, `AGENTS.md` e `docs/`
- aggiunto contratto di risposta ChatGPT
- aggiunto ingest risposta manuale
- aggiunti store workflow e lista piani
- aggiunti approve e verifica diff
- aggiunta dashboard web non bloccante
- aggiunta dockerizzazione predisposta per VPS futuro

## Prossime azioni

1. collegare Gemini a un client MCP locale
2. testare end-to-end su repository locale
3. aggiungere deploy VPS quando DuckDNS e server saranno pronti
4. aggiungere autenticazione alla web UI quando verra esposta online

## Rischi

- Gemini deve poter invocare il server MCP tramite client compatibile
- il flusso zero-cost richiede copia/incolla manuale con ChatGPT Pro
- applicazione diff deve restare controllata e approvata

## Percentuale

Core MVP: 100%
Web UI: esclusa dal conteggio core
Deploy VPS: predisposto, attivazione futura
