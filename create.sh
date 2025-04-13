#!/bin/bash
set -euo pipefail

# build and start the playground.
docker compose up --build --remove-orphans --detach
