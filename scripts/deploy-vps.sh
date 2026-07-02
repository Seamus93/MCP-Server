#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/projects/mcp-server}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"
HEALTHCHECK_URL="${HEALTHCHECK_URL:-http://localhost:8000/health}"
PROJECT_NAME="${PROJECT_NAME:-mcp-server}"
PROJECT_URL="${PROJECT_URL:-http://localhost:8000}"
REGISTER_PROJECT_SCRIPT="${REGISTER_PROJECT_SCRIPT:-/opt/infra/scripts/register-project.sh}"
HEALTHCHECK_MAX_ATTEMPTS="${HEALTHCHECK_MAX_ATTEMPTS:-12}"
HEALTHCHECK_RETRY_DELAY_SECONDS="${HEALTHCHECK_RETRY_DELAY_SECONDS:-5}"
RENDER_DOTENV_FROM_ENV="${RENDER_DOTENV_FROM_ENV:-true}"

cd "$APP_DIR"

case "$DEPLOY_BRANCH" in
  main|test|develop)
    ;;
  *)
    echo "Deploy branch '$DEPLOY_BRANCH' non consentito"
    exit 1
    ;;
esac

git config core.fileMode false

dirty_files="$(
  {
    git diff --name-only
    git diff --cached --name-only
  } | sed '/^$/d' | sort -u
)"

if [ -n "$dirty_files" ]; then
  allowed_dirty_files=$'scripts/deploy-vps.sh\n.env'
  unexpected_dirty_files="$(printf '%s\n' "$dirty_files" | grep -vxF -f <(printf '%s\n' "$allowed_dirty_files") || true)"

  if [ -n "$unexpected_dirty_files" ]; then
    echo "Worktree VPS sporco, deploy interrotto:"
    git status --short --untracked-files=no
    exit 1
  fi

  while IFS= read -r file_path; do
    [ -n "$file_path" ] || continue
    git restore --source=HEAD --staged --worktree -- "$file_path" 2>/dev/null \
      || {
        git reset -q HEAD -- "$file_path"
        git checkout -- "$file_path"
      }
  done < <(printf '%s\n' "$dirty_files")
fi

git fetch origin "$DEPLOY_BRANCH"
git checkout "$DEPLOY_BRANCH"
git pull --ff-only origin "$DEPLOY_BRANCH"

if [ "$RENDER_DOTENV_FROM_ENV" = "true" ]; then
  ./scripts/render-env-file.sh .env.example .env
fi

docker compose --env-file .env config >/dev/null
docker compose --env-file .env build
docker compose --env-file .env up -d --build

healthcheck_attempt=1
until curl -fsS "$HEALTHCHECK_URL"; do
  if [ "$healthcheck_attempt" -ge "$HEALTHCHECK_MAX_ATTEMPTS" ]; then
    echo "Healthcheck fallito dopo ${HEALTHCHECK_MAX_ATTEMPTS} tentativi: $HEALTHCHECK_URL"
    docker compose --env-file .env ps
    exit 1
  fi

  echo "Healthcheck non ancora pronto (tentativo ${healthcheck_attempt}/${HEALTHCHECK_MAX_ATTEMPTS}), nuovo tentativo tra ${HEALTHCHECK_RETRY_DELAY_SECONDS}s..."
  healthcheck_attempt=$((healthcheck_attempt + 1))
  sleep "$HEALTHCHECK_RETRY_DELAY_SECONDS"
done

if [ -x "$REGISTER_PROJECT_SCRIPT" ]; then
  "$REGISTER_PROJECT_SCRIPT" "$PROJECT_NAME" "$PROJECT_URL" "$HEALTHCHECK_URL"
fi

docker image prune -f
