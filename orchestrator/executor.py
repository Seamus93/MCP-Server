from __future__ import annotations

from pathlib import Path

from integrations.openai_client import ChatGPTDelegate
from jarvis.supervisor import JarvisSupervisor
from providers.manual_provider import ManualProvider
from workflow.project_context import ProjectContextLoader
from workflow.response_templates import CHATGPT_RESPONSE_TEMPLATE


SYSTEM_PROMPT = """Sei Jarvis, supervisor di un sistema multi-agente.
Coordina specialisti, non rispondere come modello generico.
Rispondi in italiano, in modo operativo, sintetico e strutturato.
Non dichiarare modifiche eseguite se hai solo prodotto un piano.
Se mancano informazioni, indica il prossimo input minimo necessario.
Rispetta sempre il contratto di risposta fornito nel prompt.
"""


class DelegationExecutor:
    """Builds Jarvis supervisor context and delegates reasoning to a provider."""

    def __init__(self, delegate: ChatGPTDelegate | None = None) -> None:
        self.delegate = delegate
        self.supervisor = JarvisSupervisor()

    def delegate_task(
        self,
        task: str,
        repository: str | None = None,
        repo_path: str | None = None,
        risk_level: str = "normal",
    ) -> str:
        prompt = self._build_prompt(task=task, repository=repository, repo_path=repo_path, risk_level=risk_level)
        delegate = self.delegate or ChatGPTDelegate()
        result = delegate.run(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        return result.output

    def create_manual_prompt_pack(
        self,
        task: str,
        repository: str | None = None,
        repo_path: str | None = None,
        risk_level: str = "normal",
        outbox_dir: str = ".mcp_outbox",
    ) -> str:
        context = self._build_prompt(task=task, repository=repository, repo_path=repo_path, risk_level=risk_level)
        pack = ManualProvider(outbox_dir=outbox_dir).create_prompt_pack(
            task=task,
            system_prompt=SYSTEM_PROMPT,
            context=context,
            repository=repository,
        )
        return f"Prompt pack creato: {pack.path}\n\n{pack.content}"

    def _build_prompt(self, task: str, repository: str | None, repo_path: str | None, risk_level: str) -> str:
        repo_context = self._repo_context(repo_path) if repo_path else "Nessun repository locale fornito."
        standard_context = self._standard_context(repo_path) if repo_path else "Nessuno standard locale caricato."
        supervisor_plan = self.supervisor.supervisor_prompt(task)

        return f"""
Task utente:
{task}

Repository dichiarato:
{repository or "non specificato"}

Risk level:
{risk_level}

Supervisor pattern:
{supervisor_plan}

Contesto repository locale:
{repo_context}

Standard progetto:
{standard_context}

Contratto risposta:
{CHATGPT_RESPONSE_TEMPLATE}

Regola finale:
Jarvis deve sintetizzare il lavoro degli specialisti e restituire una risposta unica, breve e adatta a essere letta da Google.
""".strip()

    @staticmethod
    def _repo_context(repo_path: str) -> str:
        root = Path(repo_path).expanduser().resolve()
        if not root.exists():
            return f"Path non trovato: {root}"
        files = []
        ignored = {".git", ".venv", "node_modules", "__pycache__", ".mcp_outbox"}
        for current_root, dirs, names in __import__("os").walk(root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for name in names:
                files.append(str((Path(current_root) / name).relative_to(root)))
                if len(files) >= 80:
                    break
            if len(files) >= 80:
                break
        return "File principali:\n" + "\n".join(files)

    @staticmethod
    def _standard_context(repo_path: str) -> str:
        return ProjectContextLoader().load(repo_path)
