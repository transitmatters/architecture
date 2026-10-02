# Tech stack

We keep projects similar so you can move between them without relearning everything.

## Frontend

- **React + TypeScript** everywhere
- **[Next.js](https://nextjs.org/)** for the bigger sites: Data Dashboard, Regional Rail Explorer, Futures Explorer, COVID Recovery Dashboard
- **[Vite](https://vite.dev/)** for smaller apps: New Train Tracker, Shutdown Tracker, Pride Bus, Station Explorer
- **Common libraries:** Tailwind, TanStack Query, Leaflet for maps, [`@transitmatters/stripmap`](../projects/libraries.md#stripmap) for line diagrams
- **Style:** ESLint + Prettier. Run `npm run lint`.
- **Node version:** in each repo's `.nvmrc`

## Backend

- **Python 3.12–3.13**
- **[Chalice](https://aws.github.io/chalice/)** for APIs and scheduled Lambda jobs
- **[uv](https://docs.astral.sh/uv/)** for packages. Some older repos still use Poetry.
- **Common libraries:** pandas, boto3, requests
- **Style:** [Ruff](https://docs.astral.sh/ruff/). Run `uv run ruff check .`
- **Exception:** Futures Explorer uses FastAPI in Docker

## Monitoring

| Tool | What for | Where |
|---|---|---|
| [Datadog](https://app.datadoghq.com/) | Logs, traces and errors for backends | Every Lambda and EC2 service |
| [GoatCounter](https://www.goatcounter.com/) | Privacy-friendly page view counts | Every public site |
| GitHub Actions | Daily health check on the Dashboard API; failed bot runs | t-performance-dash, Slow Zone Bot |

!!! note
    We don't run client-side Datadog monitoring. It would need a privacy notice.
