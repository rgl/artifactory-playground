#!/bin/bash
set -euo pipefail

docker compose down --volumes --remove-orphans --timeout=0
docker compose --profile test down --volumes --remove-orphans --timeout=0
