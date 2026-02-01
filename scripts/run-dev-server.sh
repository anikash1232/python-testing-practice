#!/usr/bin/env bash
set -euo pipefail

# Start the development server using the project-local `uv` runner
# which will invoke `uvicorn` inside the managed environment.
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
