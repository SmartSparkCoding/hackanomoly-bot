#!/usr/bin/env bash
set -euo pipefail

echo "[dev-with-db] Starting Nephthys in dev mode with local Postgres"

if ! command -v docker >/dev/null 2>&1; then
  echo "[dev-with-db] ERROR: Docker is not installed or not in PATH."
  echo "[dev-with-db] Please install Docker Desktop and retry."
  exit 1
fi

# Start or create the Postgres container
if docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres$'; then
  if ! docker ps --format '{{.Names}}' | grep -q '^hh-postgres$'; then
    echo "[dev-with-db] Starting existing Postgres container 'hh-postgres'..."
    if ! docker start hh-postgres >/dev/null 2>&1; then
      echo "[dev-with-db] Port 5432 appears in use; attempting to run Postgres on 5433..."
      if ! docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres-5433$'; then
        docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
      else
        docker start hh-postgres-5433 >/dev/null || true
      fi
      export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
      echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
    else
      export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
      echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
    fi
  else
    echo "[dev-with-db] Postgres container 'hh-postgres' is already running."
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
    echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
  fi
else
  echo "[dev-with-db] Creating Postgres container 'hh-postgres'..."
  if ! docker run --name hh-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres >/dev/null 2>&1; then
    echo "[dev-with-db] Port 5432 appears in use; creating 'hh-postgres-5433' on 5433..."
    docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
    echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
  else
    # docker run succeeded and exposed Postgres on localhost:5432
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
    echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
  fi
fi

echo "[dev-with-db] Ensuring DB and schema, then starting app"
echo "[dev-with-db] Syncing Python dependencies..."
uv sync --frozen
bash scripts/ensure-db.sh

echo "[dev-with-db] Starting app (uvicorn via script)..."
uv run nephthys
