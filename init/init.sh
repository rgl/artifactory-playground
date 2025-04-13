#!/bin/bash
set -euo pipefail

ARTIFACTORY_URL="http://artifactory:8082/artifactory"
ARTIFACTORY_REPOSITORY="example-repo-local"
ARTIFACTORY_USER="admin"
ARTIFACTORY_PASSWORD="password"

ARTIFACT_NAME="example"
ARTIFACT_VERSION="1.0.0"
ARTIFACT_FILE_NAME="$ARTIFACT_NAME-$ARTIFACT_VERSION.txt"
ARTIFACT_PROPS=(
    "name=$ARTIFACT_NAME"
    "version=$ARTIFACT_VERSION"
    "date=$(date -Iseconds)"
)
ARTIFACT_TARGET="$ARTIFACTORY_REPOSITORY/$ARTIFACT_FILE_NAME"

jf config add \
    --artifactory-url "$ARTIFACTORY_URL" \
    --user "$ARTIFACTORY_USER" \
    --password "$ARTIFACTORY_PASSWORD"

echo "Uploading artifact to $ARTIFACTORY_URL/$ARTIFACT_TARGET"
t="$(mktemp -q -d)"
ARTIFACT_PATH="$t/$ARTIFACT_FILE_NAME"
echo "This is an example artifact" > "$ARTIFACT_PATH"
jf rt upload \
    --fail-no-op \
    --target-props "$(python3 \
        /init/artifactory_encode_props.py \
        "${ARTIFACT_PROPS[@]}")" \
    "$ARTIFACT_PATH" \
    "$ARTIFACT_TARGET"
rm -rf "$t"

echo "Getting artifact details from $ARTIFACTORY_URL/$ARTIFACT_TARGET"
jf rt search "$ARTIFACT_TARGET"
