# Security

## Policy generale

Il progetto deve esporre solo tool MCP specifici, controllabili e con permessi minimi.

## Vietato

- eseguire comandi arbitrari passati dall'utente
- cancellare file senza tool dedicato e validazioni
- scrivere segreti nel repository
- usare path non validati
- fare push/merge automatici senza revisione

## Consentito

- leggere file testuali con limite caratteri
- listare directory ignorando cartelle generate
- eseguire test predefiniti
- leggere stato Git
- generare piani e checklist

## Controlli richiesti

- timeout sui processi
- path risolti con `Path.resolve()`
- output limitato
- separazione tra agenti che pianificano, scrivono e revisionano
