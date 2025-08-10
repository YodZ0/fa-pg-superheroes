#!/usr/bin/env bash

set -e

echo "[INFO] Applying migrations is running..."
alembic upgrade head
echo "[INFO] Migrations applied!"

exec "$@"