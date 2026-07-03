"""Compatibility shim: forward to backend.web.app for legacy imports."""
from backend.web.app import app

__all__ = ["app"]
