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
