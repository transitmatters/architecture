# FAQ

Questions new volunteers ask a lot. Click one to expand it.

## Finding your way

??? question "Which repo do I change for…?"

    | You want to change… | Repo |
    |---|---|
    | A chart, page or API endpoint on the dashboard | [t-performance-dash](projects/data-dashboard.md) |
    | Ridership, scheduled service, delivered trips, alerts, speed restrictions | [data-ingestion](projects/data-ingestion.md) |
    | Subway or bus events from LAMP, monthly historical files | [mbta-performance](projects/mbta-performance.md) |
    | Live bus or Commuter Rail events | [gobble](projects/gobble.md) |
    | How slow zones are detected | [slow-zones](projects/slow-zones.md) |
    | What the bot posts | [mbta-slow-zone-bot](projects/slow-zone-bot.md) |
    | The strip map component | [stripmap](projects/libraries.md#stripmap) |

    Still unsure? The [data pipeline table](architecture/data-pipeline.md#what-we-store) lists who writes every bucket and table.

??? question "Is there a good first task for me?"

    Start with the [Good First Tasks board](https://github.com/orgs/transitmatters/projects/11). There's more in [Getting started](getting-started/index.md#3-find-something-to-work-on).

## Data

??? question "Why is today (or yesterday) empty?"

    Data arrives with a delay, on purpose:

    - **Subway:** LAMP is processed every 30 minutes but starts around 6 AM, and yesterday is reprocessed in full at 15:00 UTC.
    - **Bus:** processed once a day, so today is usually missing.
    - **Summaries** (delivered trips and others) wait until 12:00 UTC, because the MBTA cleans up the previous day's data overnight.

    Expect about a day of lag. An empty result for today is usually lag, not missing service.

??? question "Why does a whole month look missing?"

    Older data comes from monthly archives, which are loaded by hand. The dashboard only shows them up to a **cutoff date** that's also moved by hand. See [Which events the dashboard reads](architecture/data-pipeline.md#which-events-the-dashboard-reads).

??? question "My query returns nothing, but the data exists"

    You're probably using the wrong ID style. `line-red`, `line-Red` and `Red` all mean the Red Line in different places. See [IDs & stations](architecture/ids.md).

??? question "Which day does a 1 AM trip belong to?"

    The previous one. A **service day** runs from about 3 AM to 3 AM Eastern, so a 1 AM Saturday trip counts as Friday.

??? question "Directions look backwards"

    They might be. Subway direction `0` in our station lists is the opposite of MBTA GTFS. See [Directions](architecture/ids.md#directions).

## Local setup

??? question "The dashboard backend gives AWS access errors"

    You have AWS credentials on your machine that aren't TransitMatters', so the backend switched to `aws` mode. Run `export TM_BACKEND_SOURCE=prod`. See [backend modes](getting-started/local-dev.md#data-dashboard-backend-modes).

??? question "Port 5000 or 5555 is already in use"

    On macOS, AirPlay Receiver uses 5000. Shutdown Tracker and New Train Tracker both use 5555. See [Ports](getting-started/local-dev.md#ports).

??? question "`npm install` fails on the dashboard"

    It requires Node 24.12 or newer, and refuses to install on older versions. Run `nvm install && nvm use` in the repo.

## Changes and deploys

??? question "Do I need AWS access?"

    Not to contribute. CI deploys everything when a PR merges. Ask in Slack if a task really needs it.

??? question "How do I test before it hits production?"

    Run it locally, and describe how you tested it in the PR. The Data Dashboard also has a [beta site](https://dashboard-beta.labs.transitmatters.org) that maintainers can deploy to.

??? question "Can my change break another project?"

    Yes. The Dashboard API is used by Shutdown Tracker, slow-zones, data-ingestion, tm-data-mcp and transitmattr. The bot and slow-zones also build links to dashboard pages. Don't rename or remove endpoints, fields or URL paths without checking those repos.

??? question "My PR needs changes in two repos"

    Common: for example, data-ingestion first, then the dashboard. Open both PRs, link them to each other, and say which must merge first. For a stripmap change, a new npm release is needed before the dashboard can use it.

??? question "My issue was marked stale"

    A bot labels issues with no activity for 180 days. Nothing is closed automatically. If you're working on it, just comment.
