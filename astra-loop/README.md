# Astra Loop

Mattermost team-edition fork rebranded as **Astra Loop**.

## Build image

```bash
./astra-loop/build.sh
```

Produces Docker image `astra-loop:dev` (override with `IMAGE_TAG=`).

## Run with Postgres

```bash
docker compose -f astra-loop/docker-compose.yml up -d
```

Open http://localhost:8065 — drop-in replacement for `mattermost-team-edition` + Postgres.

## Open-source licences

User-facing attribution lives only at `/static/oss/oss.html` (“Astra Loop includes open-source software”), linking to `LICENSE.txt` and `NOTICE.txt`.
