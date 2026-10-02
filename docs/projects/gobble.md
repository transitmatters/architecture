# gobble

Listens to the MBTA V3 streaming API around the clock and records every bus and Commuter Rail arrival and departure as event CSVs.

[Repo](https://github.com/transitmatters/gobble){ .md-button }

| | |
|---|---|
| **Stack** | Python (long-running process) |
| **Runs on** | One EC2 instance (`systemd` service) |
| **Deploys** | Push to `main` (CloudFormation + Ansible) |

```mermaid
flowchart LR
    v3(["V3 API<br/>vehicle stream"]) --> gobble["gobble<br/><small>EC2</small>"]
    gtfs(["GTFS archive"]) -- schedules --> gobble
    gobble -- "every 30 min" --> s3[("tm-mbta-performance<br/>Events-live/")]
```

## Good to know

- **Production only runs bus and Commuter Rail.** Subway events come from LAMP via [mbta-performance](mbta-performance.md).
- This is one of the few things on EC2, because it needs a constant connection.

## gobble-wrta

[gobble-wrta](https://github.com/transitmatters/gobble-wrta) adapts gobble for Worcester's WRTA buses. It polls WRTA's vehicle API and publishes dashboard-style event CSVs plus an unofficial GTFS-Realtime feed. It runs in Docker on a small DigitalOcean server, not AWS, and isn't wired into the dashboard yet.
