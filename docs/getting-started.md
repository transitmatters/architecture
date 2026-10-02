# Getting started

Welcome! TransitMatters Labs is run entirely by volunteers. Here's how to go from zero to your first merged PR.

## 1. Get connected

- **Fill out the [volunteer form](https://transitmatters.org/volunteer)** if you haven't already.
- **Join the [Labs Slack channel](https://transitmatters.slack.com/archives/GSJ6F35DW).** It's the place to ask questions, find a project and get AWS access if you need it.

## 2. Learn the shape of things

Read the [architecture overview](architecture/index.md). It takes five minutes. The key idea: most projects read from one shared data pipeline that ends in the **Data Dashboard API**.

## 3. Pick a project

| If you like… | Try |
|---|---|
| Frontend, charts, React | [Data Dashboard](projects/data-dashboard.md) |
| Something small to learn the ropes | [Pride Bus](projects/pride-bus.md) or [Shutdown Tracker](projects/shutdown-tracker.md) |
| Maps and live data | [New Train Tracker](projects/new-train-tracker.md) |
| Python and data wrangling | [data-ingestion](projects/data-ingestion.md) or [mbta-performance](projects/mbta-performance.md) |

Browse each repo's Issues for something to pick up, or ask in Slack.

## 4. Set up your machine

You'll need:

- **Git** and a GitHub account
- **Node**: use the version in the repo's `.nvmrc` (`nvm install && nvm use`)
- **Python + [uv](https://docs.astral.sh/uv/)**. A few older repos use Poetry; the README will say.
- **A free [MBTA V3 API key](https://api-v3.mbta.com/)** for apps that call the MBTA directly

!!! tip "You don't need AWS access to start"
    Most apps run locally against public data. For the Data Dashboard, `export TM_BACKEND_SOURCE=prod` points your local copy at the production API.

Most full-stack repos start with:

```bash
npm install
npm start   # runs the frontend and the Python backend together
```

## 5. Make a change

1. Create a branch and open a pull request.
2. CI runs lint and tests. Run `npm run lint` (or `uv run ruff check .`) locally first.
3. A maintainer reviews it.
4. **Merging to `main` deploys to production.** That's why reviews matter.

## Help

Stuck? Ask in Slack. Every repo also has a `CODEOWNERS` file listing who maintains it.
