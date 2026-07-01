# API

## Tool MCP correnti

### health_check

Verifica che il server MCP sia online.

### git_status

Input: `repo_path`

Restituisce `git status --short` del repository locale.

### list_files

Input: `root_path`, `max_files`

Lista file ignorando cartelle generate o pesanti.

### read_text_file

Input: `path`, `max_chars`

Legge file UTF-8 con limite caratteri.

### run_python_tests

Input: `repo_path`

Esegue `python -m pytest -q` con timeout.
