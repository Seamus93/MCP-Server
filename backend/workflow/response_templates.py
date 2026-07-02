CHATGPT_RESPONSE_TEMPLATE = """# Response Contract

Rispondi usando esattamente queste sezioni, nello stesso ordine:

## Sintesi
Una sintesi breve.

## Piano operativo
Passi numerati e verificabili.

## File da modificare
- path/file.py

## Patch proposta
Se hai una patch, usa unified diff completo. Se non hai patch, scrivi: Nessuna patch.

## Test consigliati
Comandi o verifiche.

## Rischi
Rischi tecnici o operativi.

## Prossima azione
Una sola azione concreta.
"""
