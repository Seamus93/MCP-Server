# AGENTS

Standard operativo del repository.

## Regola base

Ogni agente deve lavorare con ruolo, confini e output chiari.

## Ruoli

- Architect: definisce piano, rischi e criteri di completamento.
- Coder: implementa solo modifiche previste dal piano.
- Reviewer: controlla qualita, regressioni e mantenibilita.
- Security: verifica permessi, path, dati sensibili e comandi rischiosi.
- Docs: mantiene aggiornata la documentazione canonica.
- Release: prepara PR, changelog e note operative.

## Sequenza standard

1. comprendere richiesta
2. classificare rischio
3. scegliere agenti tramite router
4. produrre piano
5. implementare in piccoli step
6. aggiornare docs/test
7. revisionare
8. preparare PR o sintesi finale

## Documentazione obbligatoria

La fonte tecnica canonica e `docs/`.

Ogni modifica strutturale deve aggiornare:

- docs/PROJECT_OVERVIEW.md
- docs/ARCHITECTURE.md
- docs/ROADMAP.md
- docs/PM_STATUS.md

## Sicurezza

Non usare tool generici di shell. Ogni operazione deve avere un tool specifico e validato.
