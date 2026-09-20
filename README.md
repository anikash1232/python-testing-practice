# Python Testing Practice

Unit and integration tests for a FastAPI link service, covering a layered application from
storage up to HTTP.

## What it does

The application is a small link service with a clean separation between HTTP routes,
business logic, and a JSON-file-backed store. The tests exercise each layer both in
isolation and in combination.

- **Unit tests** — the store and service layers directly, with dependencies substituted
- **Integration tests** — routes through the full stack, asserting real HTTP responses
- **Fixtures** — shared setup in `conftest.py`, so tests get isolated state rather than
  leaking data into each other

## Structure

```
src/
  main.py             FastAPI application
  routes/router.py    HTTP layer
  models/link.py      domain model
  store/
    link_store.py     persistence interface
    json_file_io.py   JSON file backing
test/
  conftest.py         fixtures and shared setup
```

Splitting persistence into `link_store` (the interface) and `json_file_io` (the mechanism)
is what makes the service testable without touching the filesystem — unit tests swap in a
substitute store, while integration tests run against a temporary file supplied by a
fixture.

## Running the tests

```bash
uv sync
uv run pytest
uv run pytest --cov=src    # with coverage
```
