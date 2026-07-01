from __future__ import annotations

import os
from fastapi import Header, HTTPException, Request


def require_gateway_token(request: Request, authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("MCP_GATEWAY_TOKEN", "").strip()
    if not expected:
        return

    supplied = ""
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    if not supplied:
        supplied = request.query_params.get("token", "").strip()

    if supplied != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
