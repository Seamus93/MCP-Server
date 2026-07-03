# PM Status

## Stato

Il progetto sta passando da MCP server sperimentale a Jarvis AI Operating System personale.

Il core MVP manuale resta disponibile, ma la direzione primaria e Gateway -> Planner -> Supervisor -> Router -> Agenti -> MCP -> risposta unificata.

## Ultimo avanzamento

- aggiunto tool `gemini_task` come comando principale per Gemini
- aggiunto caricamento standard progetto da `.skills`, `AGENTS.md` e `docs/`
- aggiunto contratto di risposta ChatGPT
- aggiunto ingest risposta manuale
- aggiunti store workflow e lista piani
- aggiunti approve e verifica diff
- aggiunta dashboard web non bloccante
- aggiunta dockerizzazione predisposta per VPS futuro
- la dashboard parte da `backend.web.app:app`
- aggiunta visione Jarvis AIOS in `docs/JARVIS_AIOS.md`
- esteso registry agenti con DevOps, Analyst e Research
- esteso Router con provider, modello, MCP e tool autorizzati
- esteso Supervisor con priorita, rischio e gruppi di parallelizzazione

## Prossime azioni

1. collegare Gemini e Google Home al Jarvis Gateway
2. implementare esecuzione controllata dei Flight Plan
3. collegare provider reali alle policy del Router
4. aggiungere MCP Docker, SSH, Browser, GitHub, Google Drive, Calendar ed Email
5. aggiungere audit log e memoria persistente workflow

## Rischi

- Gemini deve poter invocare il server MCP tramite client compatibile
- il flusso zero-cost richiede copia/incolla manuale con ChatGPT Pro
- applicazione diff deve restare controllata e approvata
- deploy VPS/container deve essere riallineato alla entrypoint `backend.web.app:app`
- le policy multi-provider sono metadati finche non vengono collegate integrazioni reali
- gli MCP sensibili richiedono permessi per agente e audit prima dell'esposizione production

## Percentuale

Core MVP manuale: 100%
Kernel Jarvis AIOS: 35%
Web UI: console operativa iniziale
Deploy VPS: predisposto, da validare nel flusso DevOps
