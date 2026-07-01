# Flight Planner

## Obiettivo

Implementare il pattern Top-Down Hierarchical Planning / Supervisor-Executor.

Un planner forte genera un piano JSON strutturato. Gli agenti esecutori ricevono task atomici, riducendo errori e varianza dei modelli piccoli.

## Flusso

```text
Voce utente
  -> Jarvis Gateway
  -> Flight Planner
  -> Flight Plan JSON
  -> Work packages
  -> Specialist agents
  -> Jarvis final summary
```

## Componenti

```text
jarvis/planner.py   crea il FlightPlan JSON
jarvis/executor.py  converte i passi in work packages
```

## Endpoint

```text
GET /api/jarvis/flight-plan?task=...
```

## MCP tool

```text
create_flight_plan(task, repository, repo_path)
```

## JSON contract

```json
{
  "command_intent": "...",
  "created_at": "...",
  "planner_policy": "reasoning-heavy-planner",
  "steps": [
    {
      "step_id": 1,
      "assigned_agent": "coder",
      "action": "implement_atomic_change",
      "objective": "...",
      "parameters": {
        "repository": "...",
        "repo_path": "...",
        "model_policy": "...",
        "voice": "..."
      },
      "depends_on": [],
      "success_criteria": "..."
    }
  ],
  "final_response": {
    "agent_name": "Jarvis",
    "speech_output": "...",
    "voice_tone": "executive"
  }
}
```

## Stato attuale

Il planner e deterministico come fallback MVP. In futuro un modello reasoning top-tier potra generare lo stesso JSON contract.
