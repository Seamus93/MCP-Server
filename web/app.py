from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orchestrator.executor import DelegationExecutor
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
        items.append(
            {
                "name": path.name,
                "status": str(data.get("status", "unknown")),
                "summary": str(data.get("summary", ""))[:140],
            }
        )
    return items


@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "responses": _response_files(),
            "outbox": str(OUTBOX_DIR),
        },
    )


@app.post("/tasks/prompt-pack", response_class=HTMLResponse)
def create_prompt_pack(
    request: Request,
    task: str = Form(...),
    repository: str = Form(""),
    repo_path: str = Form(""),
    risk_level: str = Form("normal"),
) -> HTMLResponse:
    result = DelegationExecutor().create_manual_prompt_pack(
        task=task,
        repository=repository or None,
        repo_path=repo_path or None,
        risk_level=risk_level,
        outbox_dir=str(OUTBOX_DIR),
    )
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "title": "Prompt pack creato", "content": result},
    )


@app.post("/responses/ingest", response_class=HTMLResponse)
def ingest_response(
    request: Request,
    response: str = Form(...),
    response_id: str = Form(""),
) -> HTMLResponse:
    parser = ChatGPTResponseParser()
    parsed = parser.parse(response)
    path = parser.save(parsed, outbox_dir=str(RESPONSES_DIR), response_id=response_id or None)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "title": "Risposta acquisita",
            "content": f"Stato: {parsed.status}\nFile: {path}\nWarning: {', '.join(parsed.warnings) or 'none'}\n\n{parsed.to_json()}",
        },
    )


@app.post("/workflow/clear", response_class=RedirectResponse)
def clear_workflow() -> RedirectResponse:
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    for path in RESPONSES_DIR.glob("*.json"):
        path.unlink()
    return RedirectResponse(url="/", status_code=303)
