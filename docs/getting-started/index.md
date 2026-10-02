# Getting started

Welcome! TransitMatters Labs is run entirely by volunteers. Here's how to go from zero to your first merged PR.

## 1. Get connected

- **Fill out the [volunteer form](https://transitmatters.org/volunteer)** if you haven't already.
- **Join the [Labs Slack channel](https://transitmatters.slack.com/archives/GSJ6F35DW).** It's the place to ask questions, find a project and get AWS access if you need it.

## 2. Learn the shape of things

Read the [architecture overview](../architecture/index.md). It takes five minutes. The key idea: most projects read from one shared data pipeline that ends in the **Data Dashboard API**.

## 3. Find something to work on

<div class="grid cards" markdown>

-   :material-flask: **[Good First Tasks board](https://github.com/orgs/transitmatters/projects/11)**

    ---

    Hand-picked starter tasks across all our repos. **Start here.**

-   :material-magnify: **[Open "good first issue"s](https://github.com/search?q=org%3Atransitmatters+is%3Aissue+is%3Aopen+archived%3Afalse+no%3Aassignee+-label%3Astale+label%3A%22good+first+issue%22&type=issues&s=updated&o=desc)**

    ---

    Every unclaimed, recently active `good first issue` in the org.

-   :material-hand-heart: **[Open "help wanted"s](https://github.com/search?q=org%3Atransitmatters+is%3Aissue+is%3Aopen+archived%3Afalse+label%3A%22help+wanted%22&type=issues&s=updated&o=desc)**

    ---

    Bigger tasks maintainers would love help with.

</div>

Comment on an issue before you start so nobody duplicates work. If an issue is assigned but has gone quiet, ask in Slack.

Not sure which project? A rough guide:

| If you like… | Try |
|---|---|
| Frontend, charts, React | [Data Dashboard](../projects/data-dashboard.md) |
| Something small to learn the ropes | [Pride Bus](../projects/pride-bus.md) or [Shutdown Tracker](../projects/shutdown-tracker.md) |
| Maps and live data | [New Train Tracker](../projects/new-train-tracker.md) |
| Python and data wrangling | [data-ingestion](../projects/data-ingestion.md) or [mbta-performance](../projects/mbta-performance.md) |

## 4. Set up your machine

You'll need:

- **Git** and a GitHub account
- **Node**: use the version in the repo's `.nvmrc` (`nvm install && nvm use`). Some repos also pin it with [Volta](https://volta.sh/).
- **Python + [uv](https://docs.astral.sh/uv/)**. A few older repos use Poetry; the README will say.
- **A free [MBTA V3 API key](https://api-v3.mbta.com/)** for apps that call the MBTA directly

!!! tip "You don't need AWS access to start"
    Most apps run locally against public data. For the Data Dashboard, `export TM_BACKEND_SOURCE=prod` points your local copy at the production API.

Most full-stack repos start with:

```bash
npm install
npm start   # runs the frontend and the Python backend together
```

Versions, ports and test commands differ between repos. See the [local dev reference](local-dev.md).

## 5. Make a change

1. Create a branch and open a pull request. Fill in the PR template (Motivation / Changes / Testing).
2. CI runs lint and tests. Run them locally first; the [local dev reference](local-dev.md#tests-and-checks) lists the commands.
3. A maintainer reviews it.
4. **Merging to `main` deploys to production.** That's why reviews matter.

Two house rules:

- **Mention cost.** If your change could affect what we pay AWS (more Lambda calls, bigger storage, new services), say so in the PR. We run on a small nonprofit budget.
- **AI tools are fine.** Several repos include a `CLAUDE.md` with project context for AI assistants. Some repos ask you to mark AI-assisted commits with a `Co-Authored-By` line.

## Help

Stuck? Check the [FAQ](../faq.md), then ask in Slack. Every repo also has a `CODEOWNERS` file listing who maintains it.
