# Projects

Every project lives in its own repo under [github.com/transitmatters](https://github.com/transitmatters). The repo README is always the source of truth for setup.

!!! tip "Looking for something to do?"
    The [Good First Tasks board](https://github.com/orgs/transitmatters/projects/11) collects starter issues across every repo. Each repo also has a `/contribute` page, for example [t-performance-dash/contribute](https://github.com/transitmatters/t-performance-dash/contribute).

## Apps

| Project | What it does | Links |
|---|---|---|
| [Data Dashboard](data-dashboard.md) | Our flagship: charts of MBTA performance, ridership and service | [Site](https://dashboard.transitmatters.org) · [Repo](https://github.com/transitmatters/t-performance-dash) |
| [New Train Tracker](new-train-tracker.md) | Live map of the MBTA's new trains | [Site](https://traintracker.transitmatters.org) · [Repo](https://github.com/transitmatters/new-train-tracker) |
| [Shutdown Tracker](shutdown-tracker.md) | Planned subway shutdowns and how service changed after them | [Site](https://mbtashutdowns.info) · [Repo](https://github.com/transitmatters/shutdown-tracker) |
| [Slow Zone Bot](slow-zone-bot.md) | Posts new and fixed slow zones to social media | [Repo](https://github.com/transitmatters/mbta-slow-zone-bot) |
| [Regional Rail Explorer](regional-rail-explorer.md) | Compares today's Commuter Rail with a Regional Rail future | [Site](https://regionalrail.rocks) · [Repo](https://github.com/transitmatters/regional-rail-explorer) |
| [Futures Explorer](futures-explorer.md) | Trip planner and travel-time maps for proposed networks | [Site](https://futures.labs.transitmatters.org) · Private repo |
| [Station Explorer](station-explorer.md) | Facilities, accessibility and walkability for every station | [Site](https://stations.labs.transitmatters.org) · Private repo |
| [Pride Bus](pride-bus.md) | Tracks the MBTA's Pride bus | [Site](https://pridebus.transitmatters.org) · [Repo](https://github.com/transitmatters/pride-bus) |
| [COVID Recovery Dashboard](covid-recovery-dash.md) | Service and ridership since 2020 | [Site](https://recovery.transitmatters.org) · [Repo](https://github.com/transitmatters/mbta-covid-recovery-dash) |

## Data pipeline

| Project | What it does | Links |
|---|---|---|
| [data-ingestion](data-ingestion.md) | Scheduled jobs that fill most of our S3 and DynamoDB | [Docs](https://transitmatters.github.io/data-ingestion/) · [Repo](https://github.com/transitmatters/data-ingestion) |
| [mbta-performance](mbta-performance.md) | Turns MBTA LAMP data into events for the dashboard | [Repo](https://github.com/transitmatters/mbta-performance) |
| [gobble](gobble.md) | Listens to the live MBTA stream and records bus and CR events | [Repo](https://github.com/transitmatters/gobble) |
| [slow-zones](slow-zones.md) | Detects slow zones from travel times | Private repo |

## Libraries & tools

| Project | What it does | Links |
|---|---|---|
| [stripmap](libraries.md#stripmap) | React component for drawing transit line maps | [npm](https://www.npmjs.com/package/@transitmatters/stripmap) · [Repo](https://github.com/transitmatters/stripmap) |
| [mbta-gtfs-sqlite](libraries.md#mbta-gtfs-sqlite) | Python package: MBTA GTFS history as SQLite | [PyPI](https://pypi.org/project/mbta-gtfs-sqlite/) · [Repo](https://github.com/transitmatters/mbta-gtfs-sqlite) |
| [transitmattr](libraries.md#transitmattr) | R client for the Dashboard API | [Docs](https://transitmatters.github.io/transitmattr/) · [Repo](https://github.com/transitmatters/transitmattr) |
| [tm-data-mcp](libraries.md#tm-data-mcp) | Lets AI assistants query our data | Private repo |
| [walkscore-proxy](station-explorer.md#walkscore-proxy) | Keeps the Walk Score API key off the browser | [Repo](https://github.com/transitmatters/walkscore-proxy) |
| [regional-rail-schedule-generator](regional-rail-explorer.md#schedule-generator) | Builds GTFS for imagined Regional Rail service | [Repo](https://github.com/transitmatters/regional-rail-schedule-generator) |
| [gobble-wrta](gobble.md#gobble-wrta) | gobble for Worcester's WRTA buses | [Repo](https://github.com/transitmatters/gobble-wrta) |
| [lamp (fork)](mbta-performance.md#lamp) | Our contributions to the MBTA's LAMP | [Repo](https://github.com/transitmatters/lamp) |

## Other docs sites

- [data-ingestion API reference](https://transitmatters.github.io/data-ingestion/)
- [transitmattr reference](https://transitmatters.github.io/transitmattr/)
- [MBTA LAMP data dictionary](https://github.com/mbta/lamp/blob/main/Data_Dictionary.md)
- [MBTA GTFS documentation](https://github.com/mbta/gtfs-documentation/)
