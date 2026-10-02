# Architecture overview

TransitMatters Labs is a set of small, independent projects. Most of them share a single data pipeline: **we copy MBTA data into our own AWS storage, crunch it on a schedule, and serve it through the Data Dashboard API.**

## The big picture

```mermaid
flowchart LR
    subgraph sources["MBTA & MassDOT"]
        direction LR
        v3(["V3 API"])
        lamp(["LAMP"])
        gtfs(["GTFS"])
        open(["Ridership &<br/>open data"])
    end

    subgraph pipeline["Data pipeline"]
        direction LR
        gobble["gobble"]
        perf["mbta-performance"]
        ingest["data-ingestion"]
        sz["slow-zones"]
    end

    subgraph storage["Storage"]
        direction LR
        s3[("S3")]
        ddb[("DynamoDB")]
    end

    api["Data Dashboard API"]

    subgraph consumers["Built on our data"]
        direction LR
        dash("Data Dashboard")
        st("Shutdown Tracker")
        bot("Slow Zone Bot")
        tools("tm-data-mcp<br/>transitmattr")
    end

    sources --> pipeline --> storage --> api --> consumers
```

!!! info "One loop to know about"
    Some jobs (delivered trips, alert delays, slow zones) read the **API** rather than raw data, compute a summary, and write it back to storage. See [Data pipeline](data-pipeline.md#2-summaries).

## Standalone apps

These don't depend on the pipeline. They talk to MBTA data directly or ship their own.

```mermaid
flowchart LR
    v3(["MBTA V3 API"]) --> ntt("New Train Tracker") & pride("Pride Bus") & stations("Station Explorer")
    walk(["Walk Score API"]) --> wsp["walkscore-proxy"] --> stations
    gtfs(["MBTA GTFS"]) --> gen["regional-rail-schedule-generator"] --> rre("Regional Rail Explorer")
    gtfs --> fut("Futures Explorer")
    gtfs & ridership(["MBTA/MassDOT ridership"]) --> covid("COVID Recovery Dashboard")
```

## Reading the diagrams

| Shape | Means |
|---|---|
| `([ Stadium ])` | External data source |
| `[ Rectangle ]` | Code we run (jobs, APIs) |
| `[( Cylinder )]` | Storage |
| `( Rounded )` | Something people use: a site, bot or tool |

## Go deeper

- [Data sources](data-sources.md): where the raw data comes from
- [Data pipeline](data-pipeline.md): every bucket and table, and who writes and reads them
- [IDs & stations](ids.md): line, stop and direction conventions, and where station lists live
- [Hosting & deploys](hosting.md): how code gets from GitHub to production
- [Tech stack](stack.md): languages, frameworks and monitoring
