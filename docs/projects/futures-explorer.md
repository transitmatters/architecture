# Futures Explorer

A trip planner and travel-time map comparing today's network with proposed future networks.

[Open the explorer](https://futures.labs.transitmatters.org){ .md-button .md-button--primary }

!!! note "Private repo"
    Ask in Slack for access.

| | |
|---|---|
| **Stack** | Next.js + MapLibre · Python FastAPI · [MOTIS](https://github.com/motis-project/motis) routing · Docker |
| **Runs on** | One EC2 instance behind CloudFront |
| **Deploys** | Push to `main` builds images; a weekly data build triggers a redeploy |

```mermaid
flowchart LR
    gtfs(["GTFS scenarios<br/><small>committed</small>"])
    osm(["OpenStreetMap"])
    build["build-data<br/><small>GitHub Actions, weekly</small>"]
    s3[("S3<br/>tm-futures-explorer")]
    subgraph ec2["EC2 (Docker)"]
        web["Next.js"]
        api["FastAPI"]
        motis["MOTIS"]
    end
    site("futures.labs.transitmatters.org")

    gtfs & osm --> build --> s3 --> ec2
    web --> api --> motis
    ec2 --> site
```

## Good to know

- This is the only app that doesn't use Chalice. It's the most self-contained.
- Its README has a full architecture diagram and task reference.
