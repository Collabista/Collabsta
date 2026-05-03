# Collabsta backend

FastAPI service scaffold. Domain logic lives under `app/modules/`; cross-cutting pieces under `app/core/` and `app/shared/`.

**Python:** 3.12+ (see `Dockerfile` and CI).  
**Deployment:** not configured yet — no registry push or cloud provisioning in this repo.

## Planned modules

| Module | Role |
|--------|------|
| `auth` | Sessions, API keys, or OIDC (TBD) |
| `projects` | Workspaces grouping papers |
| `papers` | Upload metadata and file handles |
| `processing` | Ingestion pipeline hooks |
| `retrieval` | Search / RAG plumbing (no AI here yet) |
| `synthesis` | Literature review assembly (TBD) |
| `chat` | Q&A across papers (TBD) |
| `jobs` | Background tasks |

## Local setup

From the repository root:

```bash
cp .env.example .env   # edit values for your machine
cd backend
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install     # optional, hooks from .pre-commit-config.yaml
```

Run the API:

```bash
make dev
# or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Settings load optional `.env` from the **repository root** (`parents[3]` from `app/core/config.py`). `ENVIRONMENT` or `APP_ENV` selects the environment (CI sets `ENVIRONMENT=test`).

## Docker

Compose (Postgres + Redis for local infra):

```bash
cd backend
docker compose up -d
```

Production-style API image (no compose wiring yet):

```bash
make docker-build
# or: docker build -t collabsta-backend:test .
docker run --rm -p 8000:8000 collabsta-backend:test
```

## Make targets

| Target | Purpose |
|--------|---------|
| `make install` | Install prod + dev dependencies and `pre-commit install` |
| `make dev` | Run uvicorn with reload |
| `make lint` | `ruff check .` |
| `make format` | `ruff format .` |
| `make typecheck` | `mypy app` |
| `make test` | Pytest with coverage (`coverage.xml` in `backend/`) |
| `make security` | Bandit + pip-audit |
| `make docker-build` | Build `collabsta-backend:test` |

## CI/CD (GitHub Actions)

Workflows under `.github/workflows/`:

| Workflow | What it does |
|----------|----------------|
| `backend-ci.yml` | Ruff format/check, mypy, pytest + coverage; Postgres & Redis service containers; Python **3.12** |
| `backend-security.yml` | Bandit, pip-audit, Gitleaks (uses default `GITHUB_TOKEN`) |
| `docker-build.yml` | Builds `./backend` Dockerfile; scans image with **Trivy** (high/critical, no push) |
| `codeql.yml` | CodeQL for Python on push/PR + weekly schedule |
| `release.yml` | **Manual only** (`workflow_dispatch`): placeholder validate/build/release-notice jobs — **no production deploy** |

Path filters limit backend CI when only unrelated paths change (see each workflow). Dependabot opens grouped minor/patch PRs against **`dev`** (`/.github/dependabot.yml`).

## Security checks locally

- **Ruff** — lint + format (aligned with `pyproject.toml`).
- **Mypy** — `app` package only; Pydantic plugin enabled.
- **Bandit** — `bandit -r app -c bandit.yaml`.
- **pip-audit** — dependency CVE scan (`make security`).
- **Pre-commit** — ruff (fix + format), YAML check, EOF, trailing whitespace.

## Migrations

Alembic lives in `alembic/`. `alembic/env.py` derives the sync URL from settings (`asyncpg` → `psycopg` for migrations). Point `target_metadata` at your SQLAlchemy models when they exist, then generate revisions as usual.
