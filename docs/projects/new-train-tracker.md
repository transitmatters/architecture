# New Train Tracker

A live map of the MBTA's new Orange, Red and Green Line cars, plus when each was last seen.

[Open the tracker](https://traintracker.transitmatters.org){ .md-button .md-button--primary } [Repo](https://github.com/transitmatters/new-train-tracker){ .md-button }

| | |
|---|---|
| **Stack** | Vite + React · Python Chalice API |
| **Runs on** | S3 + CloudFront, Lambda at `traintracker-api.labs.transitmatters.org` |
| **Deploys** | Push to `main` |

```mermaid
flowchart LR
    v3(["MBTA V3 API"])
    api["API<br/><small>Lambda</small>"]
    job["UpdateLastSeen<br/><small>every 10 min</small>"]
    s3[("S3<br/>last_seen.json")]
    site("traintracker.transitmatters.org")

    v3 --> api --> site
    v3 --> job --> s3 --> api
```

## Good to know

- You need a free [MBTA V3 API key](https://api-v3.mbta.com/) to run it locally.
- It used to run on EC2. It's serverless now, so ignore old notes about SSH keys.
- The `Containerfile` is for running locally. It isn't deployed.
