#!/usr/bin/env bash
set -euo pipefail

echo "[ensure-db] Ensuring Postgres Docker container is running"

if ! command -v docker >/dev/null 2>&1; then
  echo "[ensure-db] ERROR: Docker is not installed or not in PATH."
  echo "[ensure-db] Please install Docker Desktop and retry."
  exit 1
fi

# Start or create the Postgres container
if docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres$'; then
  if ! docker ps --format '{{.Names}}' | grep -q '^hh-postgres$'; then
    echo "[ensure-db] Starting existing Postgres container 'hh-postgres'..."
    if ! docker start hh-postgres >/dev/null 2>&1; then
      echo "[ensure-db] Port 5432 appears in use; attempting to run Postgres on 5433..."
      if ! docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres-5433$'; then
        docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
      else
        docker start hh-postgres-5433 >/dev/null || true
      fi
      export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
      echo "[ensure-db] Using DATABASE_URL=${DATABASE_URL}"
    else
      export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
      echo "[ensure-db] Using DATABASE_URL=${DATABASE_URL}"
    fi
  else
    echo "[ensure-db] Postgres container 'hh-postgres' is already running."
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
    echo "[ensure-db] Using DATABASE_URL=${DATABASE_URL}"
  fi
else
  echo "[ensure-db] Creating Postgres container 'hh-postgres'..."
  if ! docker run --name hh-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres >/dev/null 2>&1; then
    echo "[ensure-db] Port 5432 appears in use; creating 'hh-postgres-5433' on 5433..."
    docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
    echo "[ensure-db] Using DATABASE_URL=${DATABASE_URL}"
  else
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/nephthys"
    echo "[ensure-db] Using DATABASE_URL=${DATABASE_URL}"
  fi
fi

echo "[ensure-db] Waiting for Postgres to be ready..."
DB_PORT="${DATABASE_URL##*:@localhost:}"
DB_PORT="${DB_PORT%%/*}"
DB_PORT="${DB_PORT:-5432}"
for i in {1..20}; do
  if nc -z localhost "${DB_PORT}" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

generate_prisma_client() {
  CI=1 PRISMA_DISABLE_TELEMETRY=1 uv run prisma generate
}

echo "[ensure-db] Generating Prisma client..."
if ! generate_prisma_client; then
  echo "[ensure-db] WARNING: prisma generate failed; clearing Prisma cache and retrying once..."
  rm -rf "${HOME}/.cache/prisma-python"
  generate_prisma_client
fi

echo "[ensure-db] Pushing Prisma schema..."
CI=1 PRISMA_DISABLE_TELEMETRY=1 uv run prisma db push --skip-generate || {
  echo "[ensure-db] WARNING: prisma db push failed (database may not be fully ready yet). Retrying once..."
  sleep 2
  CI=1 PRISMA_DISABLE_TELEMETRY=1 uv run prisma db push --skip-generate
}

echo "[ensure-db] DB ready"
