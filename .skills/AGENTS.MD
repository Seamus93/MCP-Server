AGENTS.md
Mission
Questo repository utilizza agenti AI per accelerare:
Analisi
Progettazione
Sviluppo
Testing
Deployment
Documentazione
Manutenzione
L'obiettivo è massimizzare:
Velocità di sviluppo
Qualità del codice
Sicurezza
Manutenibilità
Scalabilità
Osservabilità
Automazione
Riduzione dei costi

Priority Order
In caso di conflitto seguire sempre:
Requisiti del progetto
AGENTS.md
ADR (Architectural Decision Records)
Convenzioni del framework
Preferenze dell'agente

Decision Principles
Favorire sempre:
Soluzione più semplice
Soluzione più mantenibile
Soluzione più economica
Soluzione più documentata
Soluzione più osservabile
Soluzione più sicura
Evitare:
Overengineering
Tecnologie inutili
Dipendenze non necessarie
Complessità prematura

Project Tier Classification
Prima di progettare identificare il Tier.
Tier 1 — MVP
Obiettivo:
Validazione rapida
Ottimizzare:
Tempo
Costo
Time To Market
Accettabile:
Architettura semplice
Copertura test minima
Monitoraggio base

Tier 2 — Production
Obiettivo:
Applicazione stabile per utenti reali
Richiede:
Test
Monitoraggio
Backup
Sicurezza
CI/CD

Tier 3 — Enterprise
Obiettivo:
Alta affidabilità
Richiede:
Audit
Compliance
Disaster Recovery
Observability completa
Hardening sicurezza
Scalabilità orizzontale

AI Workflow
Prima di scrivere codice:
Analizzare requisiti
Classificare il Tier
Generare architettura
Generare schema DB
Generare roadmap
Generare issue
Generare documentazione
Solo dopo procedere all'implementazione.

Standard Technology Stack
Source Control
Git
GitHub
CI/CD
GitHub Actions
Hosting
Default:
VPS Linux
Alternative:
Cloud solo se giustificato
Reverse Proxy
Default:
Nginx
Alternative:
Traefik
Caddy

Frontend
Default:
React
Vite
TypeScript
Tailwind
Shadcn UI
TanStack Query
Alternative:
Next.js (SEO o SSR)
React Native

Backend
Default:
Node.js
TypeScript
Fastify
Alternative:
NestJS
Hono

Database
Default:
PostgreSQL

ORM
Default:
Prisma
Alternative:
Drizzle ORM

Cache
Redis

Queue
BullMQ

Authentication
Default:
Better Auth
Alternative:
Auth.js
Keycloak

AI Providers
Default:
OpenRouter
Supportati:
OpenAI
Anthropic
Gemini
DeepSeek

Email
Default:
Resend
Alternative:
Postmark

Payments
Default:
Stripe

Storage
Default:
S3 Compatible
Supportati:
Cloudflare R2
MinIO
AWS S3

Architecture Standards
Default:
Modular Monolith
Utilizzare Microservizi solo se:
esiste una motivazione documentata
è stato creato un ADR

Environment Strategy
Ogni progetto deve supportare:
local
development
staging
production
Utilizzare:
.env.example
Infisical
Mai committare:
.env
token
password
chiavi private
Struttura minima Infisical per progetto:
Project: <project-name>
Environment:
development
staging
production
Valori minimi da predisporre nel repository:
INFISICAL_PROJECT_ID
INFISICAL_ENV
INFISICAL_CLIENT_ID
INFISICAL_CLIENT_SECRET

Git Workflow
Branch principali:
main
test
Branch temporanei:
feature/*
bugfix/*
hotfix/*
Regole:
vietati commit diretti su main
merge tramite Pull Request
CI obbligatoria

Standard Repository Structure
/apps
/frontend
/backend
/packages
/shared
/ui
/prisma
/docs
/docs/adr
/.skills
/.github
/infrastructure
/scripts
/tests


VPS Infrastructure Compliance
Tutti i progetti devono essere compatibili con la VPS standard.
Struttura:
/opt/infra
/opt/projects

I progetti devono essere installati in:
/opt/projects/<project-name>

È vietato installare dentro il progetto:
Portainer
Homepage
Uptime Kuma
Grafana
Cockpit
SonarQube
Prometheus
Loki

Docker Standards
Naming Convention:
project-service

Esempi:
agriavenger-web
agriavenger-api
agriavenger-postgres

Ogni progetto deve essere deployato come Stack Docker dedicato.
Nome stack:
<project-name>

Utilizzare sempre:
Multi Stage Build
Alpine Images
Distroless quando possibile
Obiettivi:
Frontend < 200 MB
Backend Node < 500 MB
Backend Python < 700 MB

Docker Compose Standards
Ogni servizio deve avere:
restart: unless-stopped

Ogni servizio HTTP deve avere:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3


Docker Labels Standard
Ogni container deve avere:
labels:
  project.name: "<project-name>"
  project.environment: "production"
  monitoring.enabled: "true"
  homepage.group: "Projects"
  kuma.group: "Livello 2 — Applicazioni"


Health Endpoint
Ogni servizio HTTP deve esporre:
GET /health

Risposta minima:
{
  "status": "ok"
}

Risposta consigliata:
{
  "status": "ok",
  "database": true,
  "redis": true,
  "version": "1.0.0"
}


Project Registration
Ogni deploy deve eseguire:
/opt/infra/scripts/register-project.sh \
PROJECT_NAME \
PROJECT_URL \
HEALTH_URL

Lo script deve:
registrare Homepage
registrare Uptime Kuma
aggiornare VPS.md
evitare duplicati

Database Standards
Ogni tabella deve avere:
id UUID
created_at
updated_at

Valutare:
soft delete
audit trail
archiviazione
Ogni relazione deve avere:
foreign key
indice appropriato
constraint

Database Performance
Ogni:
foreign key
filtro
ricerca
ordinamento
deve essere valutato per indicizzazione.
Documentare gli indici.

CRUD Policy
Generare CRUD completi solo per entità business.
Per entità tecniche generare esclusivamente le operazioni necessarie.

Backoffice First
Per ogni Business Entity generare:
CRUD API
CRUD UI
Filtri
Ricerca
Paginazione
Export CSV
salvo diversa indicazione.
L'applicazione deve essere amministrabile da UI.

Migration Rules
Ogni modifica schema richiede:
Migrazione Prisma
Aggiornamento DB_SCHEMA.md
Aggiornamento ERD
Aggiornamento documentazione

API Standards
Default:
REST
Valutare GraphQL solo se necessario.
Ogni endpoint deve avere:
validazione input
validazione output
gestione errori
documentazione
Generare:
OpenAPI
Swagger

API Versioning
Le API pubbliche devono essere versionate.
Formato:
/api/v1/*
/api/v2/*


Quality Standards
TypeScript:
Strict Mode obbligatorio
Vietato any salvo motivazione documentata
Linting:
Biome
Formatting:
Biome
Unit Test:
Vitest
Coverage minimo:
80%

E2E:
Playwright

Pull Requests
Ogni PR deve includere:
descrizione
test eseguiti
impatto architetturale
eventuali ADR

SonarQube / SonarCloud
Default:
SonarCloud
Alternative:
SonarQube Self Hosted
Analisi obbligatorie:
Bugs
Vulnerabilities
Security Hotspots
Code Smells
Duplications
Coverage
Maintainability
Quality Gate obbligatorio.
Se fallisce:
Merge bloccato
Deploy bloccato


Security Standards
Secret Management
Utilizzare:
Infisical
Mai committare:
.env
password
token
chiavi private
Per GitHub Actions preferire l'integrazione nativa Infisical.
Autenticazione supportata:
OIDC con Machine Identity
Universal Auth con Machine Identity
Configurazione repository minima:
Repository Variables:
INFISICAL_PROJECT_ID
INFISICAL_ENV
INFISICAL_IDENTITY_ID opzionale se si usa OIDC
Repository Secrets:
INFISICAL_CLIENT_ID
INFISICAL_CLIENT_SECRET

Security Headers
Abilitare:
CSP
HSTS
X-Frame-Options
X-Content-Type-Options

Security Pipeline
Ogni repository deve includere:
CodeQL
Sonar
Trivy
Gitleaks
Dependabot
npm audit
Bloccare merge e deploy in presenza di:
Critical
High
Le GitHub Actions di security devono usare release correnti e supportate.
Quando una action viene aggiornata o sostituita, aggiornare anche AGENTS.md e la documentazione CI/CD del repository.
Se il repository GitHub non supporta Code Scanning / GitHub Advanced Security, CodeQL puo restare nella pipeline come job informativo non bloccante.
In quel caso il gate bloccante resta affidato a Sonar, Trivy, Gitleaks e npm audit.

CI/CD Standards
Generare sempre:
.github/workflows/

Default obbligatorio:
pipeline.yml

La pipeline GitHub Actions deve essere preferibilmente unica, stile stage-based, con job separati interni:
ci
sonar
security
deploy

Utilizzare workflow multipli separati solo se esiste una motivazione documentata.

Trigger standard:
push su:
main
test
pull_request
workflow_dispatch

Regole deploy:
deploy solo da main
test esegue quality/security ma non deploya

Infisical Workflow Policy:
Ogni workflow GitHub Actions deve recuperare i secret da Infisical prima degli step che dipendono dalla configurazione applicativa.
Default consigliato:
OIDC con `Infisical/secrets-action`
Fallback supportato:
Universal Auth con `INFISICAL_CLIENT_ID` e `INFISICAL_CLIENT_SECRET`

Sonar Policy:
Default SonarCloud
Il job Sonar deve partire in GitHub Actions a ogni push/PR rilevante
Il Quality Gate deve essere visibile come status check GitHub
Il merge su main deve essere bloccato se il check Sonar fallisce
Configurazione minima GitHub Actions:
SONAR_TOKEN in Repository Secrets
SONAR_ORGANIZATION come Repository Variable oppure Repository Secret, ma la pipeline deve essere coerente con la scelta
Se la pipeline usa vars.SONAR_ORGANIZATION, la variabile deve essere creata in Settings > Secrets and variables > Actions > Variables
Se la pipeline usa secrets.SONAR_ORGANIZATION, il valore deve essere creato in Repository Secrets

GitHub Actions Maintenance Policy:
Usare versioni correnti e supportate di:
actions/checkout
actions/setup-node
sonarsource/sonarqube-scan-action
aquasecurity/trivy-action
Aggiornare le versioni quando GitHub segnala deprecazioni del runtime delle actions.
Per scanner che leggono la git history o commit range, come Gitleaks, usare checkout con fetch-depth: 0 oppure un depth sufficiente a coprire il range analizzato.

Workflow Creation / Update Rule:
Ogni volta che cambia la procedura reale di:
build
security scan
quality gate
deploy
secrets/variables GitHub
secrets/variables Infisical
l'agente deve aggiornare anche:
AGENTS.md
docs/DEPLOYMENT.md
docs/SECURITY.md
se necessario docs/AGENTS_COMPLIANCE.md

Deploy Git Checkout Policy:
I file di script eseguiti dal workflow deploy devono essere committati con i permessi corretti nel repository.
Evitare `chmod` sul checkout del VPS durante la pipeline, perche puo sporcare il worktree remoto e bloccare `git checkout` o `git pull`.
Sul VPS il checkout deploy puo impostare `git config core.fileMode false` per evitare drift locali dovuti solo al bit eseguibile.
Se le uniche modifiche locali sul VPS appartengono alla whitelist di file di deploy/documentazione operativa, lo script puo autoripristinarle da `HEAD` prima del `checkout`.
Se esistono altre modifiche locali, il deploy deve fallire senza sovrascriverle.


Quality Pipeline
Lint
↓
Unit Tests
↓
Build
↓
Coverage
↓
Sonar
↓
Security Scan
↓
Deploy

Se uno step fallisce:
DEPLOY BLOCCATO


Deployment Standards
Ogni workflow deploy deve:
eseguire test
eseguire security scan
eseguire Sonar
build Docker
deploy VPS
eseguire register-project.sh

Observability Standards
Ogni progetto deve integrare:
Error Tracking
Sentry
Monitoring
Uptime Kuma
Metrics
Prometheus
Grafana
Logs
Loki

Monitoring Standards
Monitor minimi:
Frontend
Backend
Gateway
Database
Redis
quando presenti.

Backup Standards
Ogni progetto deve definire:
backup database
retention policy
recovery procedure
Backup automatici obbligatori.

Documentation Standards
Ogni repository deve contenere:
/docs

Documenti minimi:
PROJECT_OVERVIEW.md
ARCHITECTURE.md
ROADMAP.md
API.md
DB_SCHEMA.md
PM_STATUS.md
DEPLOYMENT.md
SECURITY.md


Visual Documentation
Generare sempre:
ERD
User Flow
System Flow
Deployment Flow
Utilizzare:
Mermaid
DBML

ADR
Ogni decisione architetturale deve essere registrata.
Formato:
ADR-001.md
ADR-002.md

Documentare:
contesto
decisione
conseguenze

GitHub Projects
Generare automaticamente:
Epic
Milestone
Issue
Kanban
Roadmap

PM Deliverables
Generare sempre:
Executive Summary
PM Status
Feature List
Risk Register
Roadmap
Devono essere leggibili anche da persone non tecniche.

Cost Optimization
Preferire:
VPS
Open Source
Self Hosted
Valutare SaaS solo se:
riduce significativamente il tempo
riduce il rischio
migliora la manutenzione
Documentare:
costo mensile
lock-in
alternative

Skills Registry
Le skill sono definite in:
/.skills

L'agente deve selezionare automaticamente le skill necessarie.
Skill raccomandate:
architecture
backend
frontend
database
security
devops
testing
documentation
product-manager
observability
performance
cost-optimization
ui-ux
api-design
automation
saas
crm
erp
marketplace
ai-agent


Mandatory Outputs
Per ogni nuovo progetto generare:
Executive Summary
Architettura
Repository Structure
Schema Prisma
ERD
API Contract
Roadmap
GitHub Issues
PM Status
Docker Setup
Security Plan
Backup Plan
Test Plan
Deployment Plan
Monitoring Plan
GitHub Actions
Sonar Configuration
Security Workflow
Verificare che tutti gli output siano presenti prima dell'implementazione.

Final Rule
Prima di implementare qualsiasi progetto verificare:
conformità AGENTS.md
conformità VPS Standard
conformità Security Standards
conformità CI/CD Standards
conformità Monitoring Standards
Se una sezione obbligatoria manca, l'implementazione non può iniziare.


