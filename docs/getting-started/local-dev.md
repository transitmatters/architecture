# Local dev reference

Repos don't all use the same versions or ports. Check here before you start fighting your setup.

## Versions

| Repo | Node | Python | Notes |
|---|---|---|---|
| t-performance-dash | 24 | 3.12 | `npm install` fails on older Node (`engine-strict`). `npm start` needs `wget`. |
| new-train-tracker | 22 | 3.13 | |
| shutdown-tracker | 22 | 3.13 | |
| data-ingestion | – | 3.13 | |
| gobble | – | 3.13 | Configured with `config/local.json`, not env vars |
| mbta-performance | – | 3.12 | Needs AWS credentials to run locally |
| slow-zones | – | 3.13 | |
| mbta-slow-zone-bot | – | 3.12 | README still says Poetry; it's uv |
| mbta-gtfs-sqlite | – | 3.11+ | Poetry |
| futures-explorer | 26 | 3.11 | Docker, [go-task](https://taskfile.dev/), ~10 GB disk |

You'll need both Python 3.12 and 3.13. uv fetches the right one automatically.

## Ports

| Repo | Frontend | Backend |
|---|---|---|
| t-performance-dash | 3000 | 5000 |
| shutdown-tracker | 3000 | 5555 |
| new-train-tracker | 5173 | 5555 |

- Shutdown Tracker and New Train Tracker backends **both use 5555**, so you can't run them at the same time.
- On macOS, **AirPlay Receiver uses port 5000**. If the dashboard backend won't start, turn AirPlay Receiver off in System Settings → General → AirDrop & Handoff.

## Data Dashboard backend modes

`TM_BACKEND_SOURCE` picks where the local API gets its data:

| Mode | Use when |
|---|---|
| `prod` | You don't have TransitMatters AWS access. Proxies the production API. **Most volunteers want this.** |
| `aws` | You have TransitMatters AWS access. Also `export AWS_PROFILE=transitmatters`. |
| `static` | Offline. A 90-day sample of a few stops. |

!!! warning "Set it explicitly"
    If `TM_BACKEND_SOURCE` is unset, **any** AWS credentials on your machine (a personal or work account) switch it to `aws` mode. You'll then get access errors. Set `TM_BACKEND_SOURCE=prod` to avoid this.

## Tests and checks

| Repo | Run |
|---|---|
| t-performance-dash | `npm run lint` · `cd server && uv run pytest tests/` |
| new-train-tracker | `npm run lint` · `npm run test-frontend` |
| shutdown-tracker | `npm run lint` (also fails if `shutdowns.json` isn't sorted: `npm run sort-shutdowns`) |
| data-ingestion | `AWS_DEFAULT_REGION=us-east-1 uv run pytest ingestor` |
| gobble | `uv run pytest` |
| mbta-performance | `uv run pytest mbta-performance` |
| stripmap | `npm test` |
| tm-data-mcp | `uv run pytest` |
| slow-zones, mbta-slow-zone-bot | Lint only: `uv run ruff check .` |

- **Pre-commit hooks** (Ruff) exist in most Python repos. Run `uv run pre-commit install` once after cloning; New Train Tracker does it for you.
- **Commit `package-lock.json`.** CI fails if it's out of date.
