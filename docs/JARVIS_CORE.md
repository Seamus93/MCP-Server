# Jarvis Core

## Obiettivo

Aggiungere identita agli agenti: ogni task viene associato a un agente, un tono, una voce simbolica e una policy modello.

## Componenti

```text
jarvis/registry.py   agent registry
jarvis/router.py     scelta agente da task
jarvis/formatter.py  formato risposta con metadati vocali
```

## Agenti iniziali

- Jarvis: orchestratore executive
- Architect: architettura e strategia tecnica
- Coder: implementazione
- Reviewer: revisione qualita
- Security: sicurezza operativa
- Docs: documentazione
- Release: rilascio

## Endpoint

```text
GET /api/jarvis/route?task=...
POST /api/voice-command
```

## Risposta gateway

La risposta include prefisso agente:

```text
[Architect Agent | voce=daedalus | tono=calmo, tecnico, strutturato]
```

## Uso futuro

La voce e per ora un metadato testuale. In futuro una PWA, APK o TTS potra usare `voice` per scegliere una voce diversa per ogni agente.
