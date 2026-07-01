from __future__ import annotations

from pathlib import Path

from integrations.openai_client import ChatGPTDelegate
from orchestrator.models import RoutedTask, TaskRequest
from orchestrator.router import TaskRouter


SYSTEM_PROMPT = """Sei ChatGPT dentro un MCP server usato come delegato tecnico.
Rispondi in italiano, in modo operativo, sintetico e strutturato.
Non dichiarare modifiche eseguite se hai solo prodotto un piano.
Se mancano informazioni, indica il prossimo input minimo necessario.
Output obbligatorio:
1. Sintesi
2. Piano operativo
3. Rischi
4. Prossima azione
"""


class DelegationExecutor:
    """Routes a task, builds context, and delegates reasoning to ChatGPT."""

    def __init__(self, router: TaskRouter | None = None, delegate: ChatGPTDelegate | None = None) -> None:
        self.router = router or TaskRouter()
        self.delegate = delegate or ChatGPTDelegate()

    def plan(self, task: str, repository: str | None = None, risk_level: str = "normal") -> RoutedTask:
        request = TaskRequest(
            title=task[:80],
            description=task,
            repository=repository,
            risk_level=risk_level,
        )
        return self.router.route(request)

    def delegate_task(
        self,
        task: str,
        repository: str | None = None,
        repo_path: str | None = None,
        risk_level: str = "normal",
    ) -> str:
        routed = self.plan(task=task, repository=repository, risk_level=risk_level)
        prompt = self._build_prompt(routed, repo_path=repo_path)
        result = self.delegate.run(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        return result.output

    def _build_prompt(self, routed: RoutedTask, repo_path: str | None = None) -> str:
        agents = "\n".join(
            f"- {agent.name}: {agent.mission}" for agent in routed.agents
        )
        notes = "\n".join(f"- {note}" for note in routed.execution_notes)
        repo_context = self._repo_context(repo_path) if repo_path else "Nessun repository locale fornito."

        return f"""
Task utente:
{routed.request.description}

Repository dichiarato:
{routed.request.repository or "non specificato"}

Agenti selezionati:
{agents}

Note di routing:
{notes}

Contesto repository locale:
{repo_context}

Produci un piano MVP eseguibile e sicuro.
""".strip()

    @staticmethod
    def _repo_context(repo_path: str) -> str:
        root = Path(repo_path).expanduser().resolve()
        if not root.exists():
            return f"Path non trovato: {root}"
        files = []
        ignored = {".git", ".venv", "node_modules", "__pycache__"}
        for current_root, dirs, names in __import__("os").walk(root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for name in names:
                files.append(str((Path(current_root) / name).relative_to(root)))
                if len(files) >= 60:
                    break
            if len(files) >= 60:
                break
        return "File principali:\n" + "\n".join(files)
