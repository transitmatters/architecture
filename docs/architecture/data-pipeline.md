# Data pipeline

How raw MBTA data becomes the charts on the [Data Dashboard](https://dashboard.transitmatters.org).

It happens in two steps.

## 1. Raw data in

Jobs copy MBTA data into our own storage. The API serves it from there.

```mermaid
flowchart LR
    v3(["V3 API<br/>(streaming)"])
    lamp(["LAMP"])
    gtfs(["GTFS archive"])
    open(["SharePoint &<br/>ArcGIS Hub"])

    gobble["gobble<br/><small>EC2, always on</small>"]
    perf["mbta-performance<br/><small>Lambda, every 30 min</small>"]
    ingest["data-ingestion<br/><small>Lambda, many schedules</small>"]

    events[("S3: tm-mbta-performance<br/>events, alerts")]
    tmgtfs[("S3: tm-gtfs<br/>GTFS as SQLite")]
    ddb[("DynamoDB<br/>ridership, scheduled service,<br/>speed restrictions")]

    api["Dashboard API"]

    monthly(["Monthly files<br/>(ArcGIS Hub)"])
    v3 -- "bus, CR, ferry" --> gobble --> events
    lamp -- "subway, bus" --> perf --> events
    monthly -. "by hand" .-> events
    gtfs --> ingest --> tmgtfs --> perf
    open --> ingest --> ddb
    events & ddb --> api
```

## 2. Summaries

Some jobs read the API back, compute summaries, and store them. DynamoDB summaries are served by the API; JSON files are fetched straight from the site.

```mermaid
flowchart LR
    api["Dashboard API"]
    ingest["data-ingestion<br/><small>summary jobs</small>"]
    sz["slow-zones<br/><small>daily</small>"]
    ddb[("DynamoDB<br/>delivered trips, alert delays")]
    landing[("S3: dashboard site<br/>static/landing")]
    slow[("S3: dashboard site<br/>static/slowzones")]
    site("Dashboard site")
    bot("Slow Zone Bot")

    api --> ingest --> ddb
    ingest --> landing --> site
    api --> sz --> slow --> site & bot
```

## Which events the dashboard reads

This depends on the mode and on a **cutoff date** that a maintainer moves forward by hand each time a new monthly archive is loaded.

| Mode | Up to the cutoff | After the cutoff |
|---|---|---|
| Subway | Monthly archive (`Events/monthly-data/`) | LAMP (`Events-lamp/daily-data/`) |
| Bus | Monthly archive (`Events/monthly-bus-data/`) | gobble (`Events-live/daily-bus-data/`) |
| Commuter Rail | gobble (`Events-live/daily-cr-data/`) | gobble |
| Ferry | Monthly archive (`Events/monthly-ferry-data/`) | Nothing yet |

- **Cutoffs:** `MAX_MONTH_DATA_DATE` in [`server/chalicelib/date_utils.py`](https://github.com/transitmatters/t-performance-dash/blob/main/server/chalicelib/date_utils.py) for the API. The frontend has its own `BUS_MAX_DATE`, `FERRY_MAX_DATE` and `RIDE_MAX_DATE` in [`common/constants/dates.ts`](https://github.com/transitmatters/t-performance-dash/blob/main/common/constants/dates.ts).
- **Written but not read (yet):** mbta-performance writes bus LAMP events to `Events-lamp/bus-daily-data/`, and gobble records ferry. The dashboard doesn't use either today.

## What we store

We use **S3** for files: cheap, fast, and good for large archives. We use **DynamoDB** for pre-aggregated time series, where the API needs a small slice without downloading a whole file.

| Data | Comes from | Stored in | Written by | Read by |
|---|---|---|---|---|
| Arrival/departure events | LAMP, V3 stream, monthly files | `tm-mbta-performance` `Events-lamp/`, `Events-live/`, `Events/` | mbta-performance, gobble | Dashboard API |
| GTFS snapshots | GTFS archive | `tm-gtfs` (one SQLite DB per feed) | data-ingestion | mbta-performance, data-ingestion |
| Scheduled service | GTFS | `ScheduledServiceDaily` | data-ingestion | API |
| Delivered trips | Dashboard API | `DeliveredTripMetrics` (+ `Extended`, `Weekly`, `Monthly`) | data-ingestion | API, landing page |
| Ridership | SharePoint, ArcGIS Hub | `Ridership` | data-ingestion | API |
| Alerts | V3 API, LAMP | `tm-mbta-performance` `Alerts/` | data-ingestion, mbta-performance | API |
| Alert delays | Dashboard API | `AlertDelaysDaily`, `AlertDelaysWeekly` | data-ingestion | API |
| Speed restrictions | ArcGIS Hub | `SpeedRestrictions` | data-ingestion | API (slow zone map) |
| Prediction accuracy | ArcGIS Hub | `TimePredictions` | data-ingestion | API |
| Slow zones | Dashboard API | `dashboard.transitmatters.org` `static/slowzones/` | slow-zones | Dashboard site, Slow Zone Bot |
| Landing page stats | DynamoDB | `dashboard.transitmatters.org` `static/landing/` | data-ingestion | Dashboard site |
| Travel time benchmarks | slow-zones archive | `tm-mbta-performance` `Benchmarks-tm/` | mbta-performance | API |
| Service & ridership summary | GTFS, ridership | `tm-service-ridership-dashboard` | data-ingestion | API |
| Bluebikes, weather | GBFS, Open-Meteo | `tm-bluebikes`, `tm-mbta-performance` `Weather/` | data-ingestion | Archive only, for now |

Names in `code` without a bucket are DynamoDB tables.

## Things that trip people up

- **Three event sources.** Monthly archives, LAMP and gobble all land in `tm-mbta-performance`. See [the table above](#which-events-the-dashboard-reads) for which one a chart uses.
- **Historical data is loaded by hand.** Monthly archives in `Events/` are uploaded with a [runbook](https://github.com/transitmatters/mbta-performance/blob/main/mbta-performance/chalicelib/historic/README.md), not on a schedule. After loading, bump the cutoff dates.
- **Static JSON lives in the site bucket.** Slow zones and landing page stats are written straight into the dashboard's frontend bucket, then CloudFront's cache is cleared.
- **Times are UTC.** Lambda schedules are in UTC, and most skip roughly 3–6 AM Boston time, when the T isn't running. Trust the `Cron(...)` arguments over the comments next to them; several comments are wrong.
- **A "day" is a service day.** Late-night trips belong to the previous day. The cutover is 3:00 AM Eastern in data-ingestion, gobble and mbta-performance, but 3:30 AM in the dashboard API.

## Updated by hand

These don't change on their own. If something looks frozen, check here first.

- Dashboard cutoff dates (above)
- Monthly event archives ([runbook](https://github.com/transitmatters/mbta-performance/blob/main/mbta-performance/chalicelib/historic/README.md))
- Station lists (see [IDs & stations](ids.md#station-lists))
- Shutdowns in Shutdown Tracker's `src/constants/shutdowns.json`
- New Train Tracker's fleet number ranges (`server/chalicelib/fleet.py`)
- Dashboard "peak" baselines (`common/constants/baselines.ts`)

## Key code

- Events from S3: [`t-performance-dash/server/chalicelib/data_funcs.py`](https://github.com/transitmatters/t-performance-dash/blob/main/server/chalicelib/data_funcs.py)
- GTFS ingest: [`data-ingestion/ingestor/chalicelib/gtfs/ingest.py`](https://github.com/transitmatters/data-ingestion/blob/main/ingestor/chalicelib/gtfs/ingest.py) (`ingest_feeds()`)
- All scheduled jobs: [`data-ingestion/ingestor/app.py`](https://github.com/transitmatters/data-ingestion/blob/main/ingestor/app.py) and [`mbta-performance/mbta-performance/app.py`](https://github.com/transitmatters/mbta-performance/blob/main/mbta-performance/app.py)
