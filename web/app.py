from __future__ import annotations

import json
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orchestrator.executor import DelegationExecutor
from web.schemas import VoiceCommandRequest, VoiceCommandResponse
from web.security import require_gateway_token
from workflow.response_parser import ChatGPTResponseParser

BASE_DIR = Path(__file__).resolve().parent.parent
OUTBOX_DIR = BASE_DIR / ".mcp_outbox"
RESPONSES_DIR = OUTBOX_DIR / "responses"

app = FastAPI(title="MCP-Server Dashboard")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))


def _response_files() -> list[dict[str, str]]:
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, str]] = []
    for path in sorted(RESPONSES_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"status": "invalid", "summary": "JSON non valido"}
        items.append({"name": path.name, "status": str(data.get("status", "unknown")), "summary": str(data.get("summary", ""))[:140]})
    return items


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.post("/api/voice-command", response_model=VoiceCommandResponse, dependencies=[Depends(require_gateway_token)])
def voice_command(payload: VoiceCommandRequest) -> VoiceCommandResponse:
    executor = DelegationExecutor()
    if payload.mode == "api":
        reply = executor.delegate_task(
            task=payload.command,
            repository=payload.repository,
            repo_path=payload.repo_path,
            risk_level=payload.risk_level,
        )
        return VoiceCommandResponse(status="completed", mode=payload.mode, reply=reply, next_step="Leggi la risposta all'utente.")

    reply = executor.create_manual_prompt_pack(
        task=payload.command,
        repository=payload.repository,
        repo_path=payload.repo_path,
        risk_level=payload.risk_level,
        outbox_dir=str(OUTBOX_DIR),
    )
    return VoiceCommandResponse(
        status="prompt_pack_created",
        mode="prompt_pack",
        reply=reply,
        next_step="Incolla il prompt pack in ChatGPT Pro, poi invia la risposta a /api/ingest-response.",
    )


@app.post("/api/ingest-response", dependencies=[Depends(require_gateway_token)])
def api_ingest_response(response: str, response_id: str | None = None) -> dict[str, str]:
    parser = ChatGPTResponseParser()
    parsed = parser.parse(response)
    path = parser.save(parsed, outbox_dir=str(RESPONSES_DIR), response_id=response_id)
    return {"status": parsed.status, "path": path, "warnings": ",".join(parsed.warnings)}


@app.get("/api/workflows", dependencies=[Depends(require_gateway_token)])
def api_workflows() -> list[dict[str, str]]:
    return _response_files()


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "responses": _response_files(), "outbox": str(OUTBOX_DIR)})


@app.post("/tasks/prompt-pack", response_class=HTMLResponse)
def create_prompt_pack(request: Request, task: str = Form(...), repository: str = Form(""), repo_path: str = Form(""), risk_level: str = Form("normal")) -> HTMLResponse:
    result = DelegationExecutor().create_manual_prompt_pack(
        task=task,
        repository=repository or None,
        repo_path=repo_path or None,
        risk_level=risk_level,
        outbox_dir=str(OUTBOX_DIR),
    )
    return templates.TemplateResponse("result.html", {"request": request, "title": "Prompt pack creato", "content": result})


@app.post("/responses/ingest", response_class=HTMLResponse)
def ingest_response(request: Request, response: str = Form(...), response_id: str = Form("")) -> HTMLResponse:
    parser = ChatGPTResponseParser()
    parsed = parser.parse(response)
    path = parser.save(parsed, outbox_dir=str(RESPONSES_DIR), response_id=response_id or None)
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "title": "Risposta acquisita", "content": f"Stato: {parsed.status}\nFile: {path}\nWarning: {', '.join(parsed.warnings) or 'none'}\n\n{parsed.to_json()}"},
    )


@app.post("/workflow/clear", response_class=RedirectResponse)
def clear_workflow() -> RedirectResponse:
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    for path in RESPONSES_DIR.glob("*.json"):
        path.unlink()
    return RedirectResponse(url="/", status_code=303)
