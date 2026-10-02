# Data sources

Almost everything we build starts from public MBTA and MassDOT data.

## MBTA

### [V3 API](https://www.mbta.com/developers/v3-api)

The main MBTA API. It covers system structure (lines, stops, routes) plus live vehicle positions, predictions and alerts. It also has a streaming (SSE) mode. Responses use [JSON:API](https://jsonapi.org/).

- **Used by:** New Train Tracker, Pride Bus, Station Explorer, gobble (streams every bus and Commuter Rail arrival and departure), data-ingestion (alert snapshots), Data Dashboard (live alerts, facilities)
- **Access:** free, but [get an API key](https://api-v3.mbta.com/) for anything beyond light use

### [LAMP](https://performancedata.mbta.com/)

Every subway and bus arrival and departure since September 2019, published as Parquet files. Updated throughout the day. New datasets show up regularly.

- **Used by:** mbta-performance, which turns it into the events that power most of the Data Dashboard
- **Access:** public, no key
- **Note:** LAMP is [open source](https://github.com/mbta/lamp). We contribute upstream through [our fork](https://github.com/transitmatters/lamp).

### [Static GTFS](https://www.mbta.com/developers/gtfs)

A full snapshot of the system and its schedule for a range of dates. See the [MBTA's extensions](https://github.com/mbta/gtfs-documentation/) and the [general spec](https://gtfs.org/documentation/schedule/reference/).

- **Used by:** data-ingestion (converts every feed to SQLite in the `tm-gtfs` bucket, which gives us scheduled service), mbta-performance, gobble, Regional Rail Explorer, Futures Explorer, COVID Recovery Dashboard
- **Access:** public, no key. Our `tm-gtfs` bucket needs TransitMatters AWS access.

### [GTFS-Realtime](https://www.mbta.com/developers/gtfs-realtime)

Another live view of vehicle position, heading and speed.

- **Used by:** nothing yet. We use the V3 streaming API instead. [gtfs-rt-demo](https://github.com/transitmatters/gtfs-rt-demo) is a minimal example.
- **Access:** rate-limited; API key recommended

### [SharePoint (Public Data)](https://mbta.sharepoint.com/:f:/s/PublicData/ElfNM8viGx5Out070Rg7tTABH1wLLEdwh69nIOb4J3Nt8w)

Ridership data, shared more often and in more detail than the Open Data Portal. It replaced the old Box folder.

- **Used by:** data-ingestion, which writes it to the `Ridership` table
- **Links:** [rapid transit](https://mbta.sharepoint.com/:f:/s/PublicData/ElfNM8viGx5Out070Rg7tTABH1wLLEdwh69nIOb4J3Nt8w) · [bus](https://mbta.sharepoint.com/:f:/s/PublicData/Eh1G_O3dog9Eh_EfCqsJZ9EBb6BIgjP-ovWMwdLpwuDnjw)

## MassDOT

### [Open Data Portal](https://mbta-massdot.opendata.arcgis.com/) ("Blue Book")

Periodically updated datasets about the MBTA, hosted on ArcGIS Hub.

- **Used by:** data-ingestion (speed restrictions, prediction accuracy, and Commuter Rail, ferry and RIDE ridership), mbta-performance (monthly historical events), COVID Recovery Dashboard
- **Access:** public, no key

## Everything else

| Source | Used by | For |
|---|---|---|
| [Bluebikes GBFS](https://gbfs.bluebikes.com/gbfs/gbfs.json) | data-ingestion | Station status archive |
| [Open-Meteo](https://open-meteo.com/) | data-ingestion | Hourly Boston weather |
| [Walk Score API](https://www.walkscore.com/professional/api.php) | walkscore-proxy | Station walk and bike scores |
| [OpenStreetMap](https://download.geofabrik.de/north-america/us/massachusetts.html) / [Protomaps](https://protomaps.com/) | Futures Explorer | Routing and basemaps |
| [WRTA](https://www.therta.com/) CAD/AVL + GTFS | gobble-wrta | Worcester bus events |

## Retired

!!! warning "MBTA Performance API: retired May 2024"
    It used to provide every arrival and departure for the past 90 days, and was the Data Dashboard's main source. LAMP replaced it. You'll still see references to it in older code and in the `Events/` folder in S3.

!!! warning "MassDOT ridership Box folder: no longer updated"
    A [Box folder](https://massdot.app.box.com/s/21j0q5di9ewzl0abt6kdh5x8j8ok9964) of rapid transit and bus ridership snapshots. It was replaced by the [SharePoint](#sharepoint-public-data) folder above. The COVID Recovery Dashboard still reads its historical files.
