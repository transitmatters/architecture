# IDs & stations

The most common source of "why is this empty?" Each data source names lines, stops and directions a little differently, and **the wrong one usually returns nothing instead of an error.**

## Line IDs

| Style | Example | Used by |
|---|---|---|
| Lowercase `line-` | `line-red`, `line-green`, `line-bus` | Dashboard frontend, most API endpoints |
| Capitalized `line-` (MBTA GTFS `line_id`) | `line-Red`, `line-Green` | Ridership and speed restrictions in DynamoDB |
| MBTA `route_id` | `Red`, `Green-B`, `CR-Worcester` | Alerts, delays, routes, the V3 API |

!!! warning
    Ridership with `line-red` returns `[]`. Speed restrictions with `line-red` return a 500 error. Both work with `line-Red`. [`fetch_static_data.py`](https://github.com/transitmatters/t-performance-dash/blob/main/server/scripts/fetch_static_data.py) lists all three styles side by side.

Other oddities:

- **Commuter Rail ridership** drops the `CR-` prefix: `line-Worcester`.
- **Combined bus routes** are `17/19` in the UI and `17-19` in file names.

## Stop IDs

| Mode | Event files | Example |
|---|---|---|
| Subway | Child stop (one platform) | `70061` |
| Subway (station) | Parent station | `place-brntn` |
| Bus | `{route}-{direction}-{stop}` | `1-0-110` |
| Commuter Rail | `{route}_{direction}_{stop}` | `CR-Worcester_0_WML-0364-01` |
| Ferry | `_` in live files, `\|` in monthly files | `Boat-F4_0_…` / `Boat-F4\|0\|…` |

- Subway terminals often use one stop ID for both directions.
- LAMP sometimes reports platform names such as `Alewife-01`. mbta-performance maps these back to numeric IDs.

## Directions

!!! danger "Subway direction keys are flipped"
    In the dashboard's `stations.json`, subway direction `"0"` is **northbound** (or eastbound for Green). In MBTA GTFS, `direction_id` 0 is **southbound** for Red and Orange, and **westbound** for Green and Blue. Event files use the GTFS value. Don't match one to the other directly.

Bus, Commuter Rail and ferry follow GTFS: `0` is outbound.

## Station lists

There is no single list. These copies have drifted apart:

| Copy | Notes |
|---|---|
| [`t-performance-dash/common/constants/stations.json`](https://github.com/transitmatters/t-performance-dash/blob/main/common/constants/stations.json) | **The source of truth.** Also served publicly at `/api/routes` and `/api/stops/{route_id}`. |
| `slow-zones/resources/stations.json` | Adds `grade_separated`. Green Line slow zones are only computed between grade-separated stations. |
| [`shutdown-tracker/src/constants/stations.json`](https://github.com/transitmatters/shutdown-tracker/blob/main/src/constants/stations.json) | Names in `shutdowns.json` must match this copy. |
| [`mbta-slow-zone-bot/stations.json`](https://github.com/transitmatters/mbta-slow-zone-bot/blob/main/stations.json) | Trimmed copy for post text |
| [`data-ingestion/ingestor/chalicelib/stations.py`](https://github.com/transitmatters/data-ingestion/blob/main/ingestor/chalicelib/stations.py) | Python version, used for trip metrics |

## Adding or changing a station or route

When the MBTA opens a station or changes routes (for example, the bus network redesign), expect to touch several repos:

1. **Dashboard:** `common/constants/stations.json` (subway) or `common/constants/bus_constants/*.json` (bus), plus line types and baselines. The [historic data runbook](https://github.com/transitmatters/mbta-performance/blob/main/mbta-performance/chalicelib/historic/README.md#when-a-route-or-station-changes) has the full list, including the bus manifest scripts.
2. **gobble:** bus stops are only recorded if they're in `BUS_STOPS` in [`src/constants.py`](https://github.com/transitmatters/gobble/blob/main/src/constants.py).
3. **The other station lists above**, if the change affects slow zones, shutdowns or the bot.

Ask in Slack before starting. It's easy to miss a copy.
