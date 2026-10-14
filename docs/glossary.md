# Glossary

## Transit

**Headway**
:   Time between consecutive vehicles at a stop.

**Dwell**
:   How long a vehicle sits at a stop.

**Travel time**
:   Time to get from one stop to another.

**Slow zone**
:   A stretch of track where trains are consistently slower than normal. We detect these from travel times.

**Speed restriction**
:   An official MBTA order to run slower on a stretch of track. Often the cause of a slow zone.

**Service day**
:   The MBTA's operating day, which runs from about 3 AM to 3 AM Eastern. A 1 AM trip belongs to the previous day.

**Delivered trips / service**
:   How many trips actually ran, compared with how many were scheduled.

**CR**
:   Commuter Rail.

**The RIDE**
:   The MBTA's paratransit service.

## Data

**GTFS**
:   General Transit Feed Specification: the standard format for schedules, stops and routes. See [Data sources](architecture/data-sources.md#static-gtfs).

**GTFS-RT**
:   GTFS-Realtime: live vehicle positions and predictions.

**V3 API**
:   The MBTA's main developer API.

**LAMP**
:   The MBTA's published performance data: every arrival and departure.

**Events**
:   Our name for arrival/departure records, stored as CSVs in S3.

**Parent station / child stop**
:   A station (`place-pktrm`) contains one child stop per platform (`70075`). Event files use child stops. See [IDs & stations](architecture/ids.md).

**Blue Book**
:   MassDOT's open data portal.

## Infrastructure

**Chalice**
:   An AWS framework for writing Python Lambda apps that look like Flask.

**Lambda**
:   AWS's "run this function on demand" service. We pay only when it runs.

**S3**
:   AWS file storage.

**DynamoDB**
:   AWS's NoSQL database. We use it for pre-aggregated time series.

**CloudFront**
:   AWS's CDN. It sits in front of our S3-hosted sites.

**CloudFormation**
:   AWS infrastructure-as-code. Each app's `deploy.sh` updates its stack.

**Beta**
:   A copy of an app at `*-beta.labs.transitmatters.org`, for testing before production.
