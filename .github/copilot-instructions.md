<!-- Copilot / AI agent guidance for the SASS repository -->
# Quick orientation for AI coding agents

This repo is a small FastAPI-based Student Assignment Submission System. Use these notes to be productive quickly and avoid making unsafe assumptions.

- **Entry point:** [app/main.py](app/main.py#L1) — FastAPI `app` is defined here and a handful of top-level routes are present.
- **Routers:** look under [app/api/v1/](app/api/v1/users.py#L1) — real route implementations live there (some files are currently empty).
- **Schemas:** Pydantic models are in [app/schemas](app/schemas/user.py#L1) (Pydantic v2-style `BaseModel`).
- **DB layer:** SQLAlchemy models under [app/models](app/models/users.py#L1); DB session/config in [app/database/session.py](app/database/session.py#L1) and [app/database/base.py](app/database/base.py#L1).
- **Config:** environment-driven via [app/core/config.py](app/core/config.py#L1). `DATABASE_URL` comes from `.env` / environment.
- **Migrations:** Alembic is present (`alembic/`, `alembic.ini`) — use `alembic` commands for schema changes.
- **Deps:** See `requirements.txt` for pinned packages (FastAPI, SQLAlchemy, Uvicorn, Pydantic, etc.).

Important patterns and examples
- Database models use declarative SQLAlchemy `Base` from [app/database/base.py](app/database/base.py#L1) and are declared in `app/models/*` (e.g., `User`, `Assignment`).
- Request/response validation uses Pydantic schemas from `app/schemas` (e.g., `UserCreate`, `UserUpdate`). Prefer schema changes over raw dicts when adding endpoints.
- Router functions use FastAPI dependencies for DB access via `get_db()` (see [app/database/base.py](app/database/base.py#L1)).

Developer workflows (commands)
- Install deps: `pip install -r requirements.txt` (see [requirements.txt](requirements.txt#L1)).
- Run dev server: `uvicorn app.main:app --reload --port 8000` (the FastAPI `app` object is in `app/main.py`).
- Run migrations: `alembic upgrade head` (alembic config is at `alembic.ini`).

Project-specific conventions and caveats
- Schemas are authoritative for API shapes — update `app/schemas/*` when changing request or response formats.
- Database URL is provided via `DATABASE_URL` (see [app/core/config.py](app/core/config.py#L1)); avoid hardcoding DB credentials.
- Many modules contain TODOs or incomplete implementations (empty files or inconsistent names). Example issues found during discovery:
  - `app/database/session.py` defines `SassionLocal` (typo) instead of `SessionLocal`.
  - `app/models/users.py` uses the field `harshed_password` (typo) while other code references `hashed_password`.
  - `app/database/base.py` references undefined symbols like `SessionLocal` and `User` in helper functions.

Guidance for automated changes
- Prefer small, focused edits and open a PR describing motivation and tests. Don't refactor multiple layers in one change.
- When fixing naming or API inconsistencies, update both schema/model and usages. Run the app and alembic migrations locally to verify.
- Add tests or a minimal local verification step for behavioral changes — there is no test suite in the repo yet.

Where to look first when implementing features
- Add new endpoints: implement router logic under `app/api/v1/` and use Pydantic schemas from `app/schemas`.
- DB interactions: update models in `app/models/` and create/modify migrations using Alembic.
- Authentication/authorization: `app/core/security.py` and `app/core/dependencies.py` are placeholders — check for any existing token patterns before adding a new scheme.

If something is unclear
- Ask for the target environment details (DB used locally vs hosted, expected auth behavior). When in doubt, propose a small PR and request quick manual verification.

If you'd like, I can:
- run a quick pass to normalize `SessionLocal` / `hashed_password` names and add unit smoke-tests,
- or draft a CONTRIBUTING snippet with exact dev commands.

— End of guidance
