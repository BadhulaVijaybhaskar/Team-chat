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

## Legal notices

After sign-in, Help → **Legal notices** (or the About dialog) opens `/static/oss/oss.html`. That page holds the Apache NOTICE, AGPLv3 notice, and AGPL §13 corresponding-source offer. Pre-sign-in surfaces (login, signup, footer, error pages, emails) do not show licence or upstream project names.

See [`LICENSE_NOTES.md`](../LICENSE_NOTES.md).
