# About

[![Test](https://github.com/rgl/artifactory-playground/actions/workflows/test.yaml/badge.svg)](https://github.com/rgl/artifactory-playground/actions/workflows/test.yaml)

Artifactory OSS playground.

**NB** Artifactory OSS only supports Maven/Gradle/Ivy/SBT/Generic repositories.

# Usage

Install docker and docker compose.

Create the playground:

```bash
./create.sh
```

Open the Artifactory UI:

http://localhost:8082

Login as:

Username: `admin`
Password: `password`

Inspect the `example-1.0.0.txt` artifact (also look at its properties):

http://localhost:8082/ui/repos/tree/General/example-repo-local/example-1.0.0.txt

Inspect the database:

```bash
# show artifact properties.
docker compose exec -T postgres psql -U artifactory <<'EOF'
\d+ nodes
\d+ node_props
select node_type, repo, node_path, node_name from nodes;
select n.repo, n.node_path, n.node_name, p.prop_key, p.prop_value
from nodes as n inner join node_props as p on n.node_id=p.node_id
where n.node_type=1;
EOF
# dump the schema.
docker compose exec -T postgres pg_dump -U artifactory --schema-only artifactory
# dump the schema and data.
docker compose exec -T postgres pg_dump -U artifactory artifactory
```

Destroy everything:

```bash
./destroy.sh
```
