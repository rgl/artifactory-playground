#!/bin/bash
set -euo pipefail

docker compose --profile test run --build --remove-orphans tests
