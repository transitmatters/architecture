# Libraries & tools

Shared code and ways to use our data outside the dashboard.

## stripmap

[`@transitmatters/stripmap`](https://www.npmjs.com/package/@transitmatters/stripmap) is a React and SVG component for drawing a transit line as a schematic strip map. The Data Dashboard uses it for the slow zone map.

- **Publish:** bump the version in `package.json` and merge. CI publishes to npm.
- **Develop:** `npm run storybook`
- [Repo](https://github.com/transitmatters/stripmap)

## mbta-gtfs-sqlite

A Python package on [PyPI](https://pypi.org/project/mbta-gtfs-sqlite/) that downloads the MBTA's GTFS history, converts each feed to SQLite, and lets you query it with SQLAlchemy. data-ingestion uses it to build the `tm-gtfs` bucket.

- **Publish:** bump the version in `pyproject.toml` and merge.
- [Repo](https://github.com/transitmatters/mbta-gtfs-sqlite)

## transitmattr

An R client for the Dashboard API, with a [full reference site](https://transitmatters.github.io/transitmattr/).

```r
pak::pak("transitmatters/transitmattr")
```

- [Repo](https://github.com/transitmatters/transitmattr)

## tm-data-mcp

An [MCP](https://modelcontextprotocol.io/) server that lets AI assistants (Claude, Cursor, …) answer MBTA questions using the Dashboard API. You run it on your own machine; it isn't hosted anywhere.

!!! note "Private repo"
    Ask in Slack for access.
