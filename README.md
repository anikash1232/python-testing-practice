# COMP423 Base Dev Container

The purpose of this dev container is to serve as a starting point for COMP423 projects driven by Architectural Design Records.

## Development — Dev Container

- **Dev Container:** A minimal VS Code Dev Container is provided at [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json).
- **Image (pinned):** The container is pinned to Microsoft-supported Python `3.14` using `mcr.microsoft.com/devcontainers/python:3.14`.
- **Why pinned:** Pinning to `3.14` ensures a reproducible Python runtime across developer machines and CI while remaining on the latest stable Python supported by the Dev Containers images.
- **Recommended extensions:** The container suggests `ms-python.python` and `ms-python.vscode-pylance`.
- **Usage:** In VS Code, choose _Remote-Containers: Open Folder in Container..._ and open the repository root to start the container.

## Dependencies — `uv`

This repository uses `uv` for dependency and virtual environment management (see [docs/arch/adr001-uv-for-dependency-management.md](docs/arch/adr001-uv-for-dependency-management.md)).

- Sync dependencies (uses the checked-in `uv.lock`): `uv sync --frozen`
- Run the script in the managed environment: `uv run python src/main.py`

## Development server

- Start the development server (uses the project-local `uv` runner to invoke `uvicorn`):

```bash
# from the repository root
./scripts/run-dev.sh
```

After doing so, you can access the dev server's OpenAPI interface by navigating to VSCode's Ports pane, looking for 8000, opening the forwarded address on your host machine (clickable link) and adding `/docs` to the end of the URL.

## Testing — `pytest`

This repository uses `pytest` for automated tests (see [docs/arch/adr002-pytest-for-automated-tests.md](docs/arch/adr002-pytest-for-automated-tests.md)).

- Install dev dependencies: `uv sync --group dev`
- Run tests (unit tests by default): `uv run pytest`
- Run tests with coverage: `uv run pytest --cov=src --cov-report=term-missing`
- Run integration tests: `uv run pytest --integration`
- Run all tests: `uv run pytest --integration`

## Type Checking — `pyright`

This repository uses `pyright` for static type checking (see [docs/arch/adr003-pyright-for-type-checking.md](docs/arch/adr003-pyright-for-type-checking.md)).

- Run type checking: `uv run pyright --project pyproject.toml`

## Linting & Formatting — `ruff`

This repository uses `ruff` for linting and formatting (see [docs/arch/adr004-ruff-for-linting-formatting.md](docs/arch/adr004-ruff-for-linting-formatting.md)).

- Install dev dependencies: `uv sync --group dev`
- Format code: `uv run ruff format .`
- Check formatting (CI-style): `uv run ruff format --check .`
- Lint: `uv run ruff check .`
- Lint + auto-fix safe issues: `uv run ruff check --fix .`

## Quality Assurance — Run All Checks

Run all quality checks in sequence (format, lint, type check, and test) using the QA script:

```bash
# from the repository root
./scripts/run-qa.sh
```

The script will run the following steps in order and fail at the first failing step:
1. Format code with `ruff format`
2. Auto-fix linting issues with `ruff check --fix`
3. Check for remaining linting issues with `ruff check`
4. Type check the `src` directory with `pyright`
5. Run unit tests with `pytest`
6. Run all tests (including integration tests) with coverage report

This is particularly useful before committing changes or opening a pull request.
