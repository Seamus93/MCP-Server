import pytest


pytest.importorskip("fastapi")
pytest.importorskip("jinja2")
pytest.importorskip("multipart")


def test_home_template_renders_through_backend_import() -> None:
    from fastapi.testclient import TestClient
    from backend.web.app import app

    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "Jarvis AIOS" in response.text


def test_voice_command_handles_missing_repo_path() -> None:
    from fastapi.testclient import TestClient
    from backend.web.app import app

    response = TestClient(app).post(
        "/api/voice-command",
        json={
            "command": "Dimmi lo stato del progetto",
            "repository": "Seamus93/MCP-Server",
            "repo_path": "/path/that/does/not/exist",
            "risk_level": "normal",
            "mode": "prompt_pack",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "prompt_pack_created"
