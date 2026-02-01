## Project Overview

- **Language Runtime:** Python 3.14 (dev container)
- **Dependency manager:** `uv`
- **Web framework:** FastAPI (served with `uvicorn`)
- **QA tools:** `ruff`, `pyright`, `pytest`, `pytest-cov`

## Repository Structure

- **Architectural Design Records:** [docs/arch/](docs/arch/)
- **Source code:** [src/](src/)
    - **Routes:** [src/routes/](src/routes/)
    - **Models:** [src/models/](src/models/)
    - **Storage:** [src/store/](src/store/)
    - **Scripts:** [scripts/](scripts/)
- **Tests:** [test/](test/)

## Automated QA Tooling

- Unit tests: `uv run pytest`
- Integration tests: `uv run pytest --integration`
- Test coverage: `uv run pytest --cov=src --cov-report=term-missing`
- Type check: `uv run pyright --project pyproject.toml`
- Format: `uv run ruff format .`
- Auto-fix safe linting issues: `uv run ruff check --fix .`
- Lint without fixing: `uv run ruff check .`
- QA script has all automated checks: `./scripts/run-qa.sh`

## Development Conventions

- Use Google-style Python documentation standards with simple, direct language.
- Follow existing module organization in `src/`.
- Keep public APIs stable unless the change request explicitly allows it.
- Prefer small, focused edits and avoid reformatting unrelated code.
- Update or add tests for changed or added behavior.
- Unit tests are in the test files whose names end with `_unit.py`. Integration tests end with `_integration.py`.
- Unit tests must be fully isolated from dependencies.
- Integration tests are marked with `@pytest.mark.integration`.
- 100% test coverage of code in the `src/` directory is required.

## Agent Conventions

- Source the virtual environment `.venv` when running terminal commands.
- Create step-by-step plan before making any changes.
- Do not add any dependencies unless specifically asked. Document any new dependency choice.
- Before completing a task always run `./scripts/run-qa.sh` as the final step. If issues arise in the QA tests, try to understand and explain why before asking the user if they would like you to attempt to fix the issue for them.
