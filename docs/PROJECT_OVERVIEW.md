# Project Overview

## Executive Summary

MCP-Server evolve in Jarvis, un AI Operating System personale per orchestrare modelli AI, agenti, MCP, memoria, workflow e interfacce di ingresso.

Jarvis riceve richieste da API, dashboard, voce, Google Home, Gemini o webhook, pianifica il lavoro, sceglie agenti e strumenti, poi restituisce una risposta unica senza esporre all'utente quale modello o tool e stato usato.

## Tier

- classificazione: `Tier 1 - AIOS Prototype`
- motivazione: kernel Jarvis in evoluzione, con Gateway FastAPI, Planner, Supervisor, Router e agenti specializzati in fase di consolidamento

## Utenti

- sviluppatore owner del repository
- agenti AI collegati tramite MCP client
- assistente vocale e Google Home come front-end operativo
- webhook e dashboard come ingressi controllati

## Funzionalita correnti

- Jarvis Gateway FastAPI canonico `backend.web.app:app`
- Planner deterministico con contratto Flight Plan
- Supervisor multi-agente con priorita, rischio e parallelizzazione
- Router con selezione automatica di agente, provider, modello, MCP e tool
- MCP server Python minimale
- dashboard web FastAPI esposta da `backend.web.app:app`
- tool sicuri per filesystem, git status e test Python
- prompt base per agenti specializzati
- registry agentico con MCP autorizzati per agente
- CI GitHub Actions

## Dipendenze esterne

- Python
- MCP SDK
- FastAPI
- pytest
- Git
- GitHub
- provider AI configurabili tramite policy del Router

## Vincoli di delivery

- tool con permessi minimi
- niente comandi arbitrari generici
- documentazione tecnica obbligatoria in `docs/`
- standard operativo allineato alla directory `.skills/`
- gli avvii web devono usare `backend.web.app:app`
