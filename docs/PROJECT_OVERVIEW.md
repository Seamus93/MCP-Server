# Project Overview

## Executive Summary

MCP-Server e un server MCP sperimentale per orchestrare agenti specializzati su repository GitHub e workflow di sviluppo.

## Tier

- classificazione: `Tier 1 - Prototype`
- motivazione: progetto in fase iniziale, nessun ambiente production, focus su architettura e standard operativo

## Utenti

- sviluppatore owner del repository
- agenti AI collegati tramite MCP client
- assistente vocale usato come front-end operativo

## Funzionalita correnti

- MCP server Python minimale
- tool sicuri per filesystem, git status e test Python
- prompt base per Architect, Coder, Reviewer
- router agentico rule-based
- CI GitHub Actions

## Dipendenze esterne

- Python
- MCP SDK
- pytest
- Git
- GitHub

## Vincoli di delivery

- tool con permessi minimi
- niente comandi arbitrari generici
- documentazione tecnica obbligatoria in `docs/`
- standard operativo allineato alla directory `.skills/`
