from diagrams import Cluster, Diagram, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.database import DynamodbTable
from diagrams.saas.logging import DataDog
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import React
from diagrams.custom import Custom
from diagrams.onprem.vcs import Github
from diagrams.aws.compute import EC2Instance

from logos import mbta_icon, massdot_icon, box_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")
s3_read = Edge(color="darkgreen", fontcolor="darkgreen", xlabel="s3 read", minlen="3")
s3_write = Edge(color="darkorange", fontcolor="darkorange", xlabel="s3 write", minlen="4")
dynamo_read = Edge(color="olive", fontcolor="olive", xlabel="dynamo read", minlen="3")
dynamo_write = Edge(color="slateblue", fontcolor="slateblue", xlabel="dynamo write", minlen="4")


def full():
    with Diagram("TransitMatters - Full Architecture", filename="diagrams/transitmatters_full_architecture", graph_attr=graph_attr, show=False):

        with Cluster("MBTA"):
            mbta_performance_api = Custom("MBTA Performance API", mbta_icon)
            mbta_v3_api = Custom("MBTA v3 API", mbta_icon)
            mbta_gtfs = Custom("MBTA GTFS", mbta_icon)
            mbta_gtfs_rt = Custom("MBTA GTFS-RT", mbta_icon)
            mass_dot_blue_book = Custom("MassDOT Blue Book", massdot_icon)
            mass_dot_box = Custom("MassDOT Box", box_icon)

        with Cluster("t-performance-dash"):
            data_dashboard_api = LambdaFunction("Data Dashboard API")
            data_dashboard_frontend = React("Data Dashboard Frontend")
            data_dashboard_api - data_dashboard_frontend

        with Cluster("data-ingestor"):
            ingestor_bb_store_station_info = LambdaFunction("BbStoreStationInfo")
            ingestor_bb_store_station_status = LambdaFunction("BbStoreStationStatus")
            ingestor_bb_calc_daily_stats = LambdaFunction("BbCalcDailyStats")
            ingestor_store_new_train_runs = LambdaFunction("StoreNewTrainRuns")
            ingestor_store_yesterdays_alerts = LambdaFunction("StoreYesterdayAlerts")
            ingestor_populate_delivered_trip_metrics = LambdaFunction("PopulateDeliveredTripMetrics")
            ingestor_populate_agg_delivered_trip_metrics = LambdaFunction("PopulateAggDeliveredTripMetrics")
            ingestor_update_delivered_trip_metrics = LambdaFunction("UpdateDeliveredTripMetrics")
            ingestor_update_delivered_trip_metrics_yesterday = LambdaFunction("UpdateDeliveredTripMetricsYesterday")
            ingestor_update_agg_trip_metrics = LambdaFunction("UpdateAggTripMetrics")
            ingestor_update_gtfs = LambdaFunction("UpdateGtfs")
            ingestor_update_ridership = LambdaFunction("UpdateRidership")
            ingestor_update_speed_restrictions = LambdaFunction("UpdateSpeedRestrictions")
            ingestor_store_landing_data = LambdaFunction("StoreLandingData")
            ingestor_update_time_predictions = LambdaFunction("UpdateTimePredictions")

        with Cluster("slow-zones"):
            slow_zone_lambda = LambdaFunction("SlowZonesLambda")

        with Cluster("mbta-slow-zone-bot"):
            slow_zone_bot = GithubActions("Slowzone Bot")

        with Cluster("regional-rail-explorer"):
            regional_rail_explorer = React("Regional Rail Explorer")

        with Cluster("mbta-covid-recovery-dash"):
            covid_recovery_dash = React("COVID Recovery Dashboard")

        with Cluster("new-train-tracker"):
            new_train_tracker = React("New Train Tracker")

        with Cluster("AWS", graph_attr={"margin": "35"}):
            with Cluster("S3"):
                data_dashboard_bucket = S3("dashboard.transitmatters.org")
                bluebikes_bucket = S3("tm-bluebikes")
                tm_mbta_performance_bucket = S3("tm-mbta-performance")
                tm_gtfs = S3("tm-gtfs")

            with Cluster("DynamoDB"):
                dynamo_delivered_trip_metrics = DynamodbTable("DeliveredTripMetricsDB")
                dynamo_delivered_trip_metrics_weekly = DynamodbTable("DeliveredTripMetricsWeeklyDB")
                dynamo_delivered_trip_metrics_monthly = DynamodbTable("DeliveredTripMetricsMonthlyDB")
                dynamo_scheduled_service_daily = DynamodbTable("ScheduledServiceDaily")
                dynamo_ridership = DynamodbTable("Ridership")
                dynamo_speed_restrictions = DynamodbTable("SpeedRestrictions")
                dynamo_time_predictions = DynamodbTable("TimePredictions")
                # DynamodbTable("OverviewStats")
                # DynamodbTable("DailySpeedDB")
                # DynamodbTable("WeeklySpeedDB")
                # DynamodbTable("MonthlySpeedDB")
                # DynamodbTable("TripCounts")

            with Cluster("EC2"):
                ec2_ntt = EC2Instance("ntt-traintracker.transitmatters.org")
                ec2_rre = EC2Instance("rre-regionalrail.rocks")

        with Cluster("GitHub"):
            github_pages = Github("GitHub Pages")

        datadog = DataDog("Datadog")

        # API Edges
        mbta_performance_api >> standard_edge >> data_dashboard_api
        mbta_performance_api >> standard_edge >> ingestor_store_new_train_runs
        mbta_performance_api >> standard_edge >> slow_zone_lambda
        mbta_v3_api >> standard_edge >> new_train_tracker
        mbta_gtfs >> standard_edge >> ingestor_update_gtfs
        mbta_gtfs >> standard_edge >> covid_recovery_dash
        mass_dot_box >> standard_edge >> ingestor_update_ridership
        mass_dot_box >> standard_edge >> covid_recovery_dash
        mass_dot_blue_book >> standard_edge >> ingestor_update_speed_restrictions

        # EC2 Instances
        new_train_tracker >> standard_edge >> ec2_ntt
        regional_rail_explorer >> standard_edge >> ec2_rre

        # S3 Connections
        data_dashboard_bucket >> s3_read >> slow_zone_bot
        slow_zone_lambda >> s3_write >> data_dashboard_bucket
        data_dashboard_bucket >> s3_read >> data_dashboard_frontend

        # Ingestor to S3 Connections
        ingestor_bb_store_station_status >> s3_write >> bluebikes_bucket
        ingestor_bb_store_station_info >> s3_write >> bluebikes_bucket
        ingestor_bb_calc_daily_stats >> s3_write >> bluebikes_bucket
        ingestor_store_new_train_runs >> s3_write >> tm_mbta_performance_bucket
        ingestor_store_yesterdays_alerts >> s3_write >> tm_mbta_performance_bucket
        ingestor_update_gtfs >> s3_write >> tm_gtfs
        ingestor_store_landing_data >> s3_write >> data_dashboard_bucket

        # Dynamo Connections
        dynamo_scheduled_service_daily >> dynamo_read >> data_dashboard_api
        dynamo_ridership >> dynamo_read >> data_dashboard_api
        dynamo_speed_restrictions >> dynamo_read >> data_dashboard_api
        dynamo_time_predictions >> dynamo_read >> data_dashboard_api
        dynamo_delivered_trip_metrics >> dynamo_read >> data_dashboard_api
        dynamo_delivered_trip_metrics_weekly >> dynamo_read >> data_dashboard_api
        dynamo_delivered_trip_metrics_monthly >> dynamo_read >> data_dashboard_api
        dynamo_delivered_trip_metrics_weekly >> dynamo_read >> ingestor_store_landing_data
        dynamo_ridership >> dynamo_read >> ingestor_store_landing_data

        # Ingestor to Dyanmo Connections
        ingestor_update_gtfs >> dynamo_write >> dynamo_scheduled_service_daily
        ingestor_update_ridership >> dynamo_write >> dynamo_ridership
        ingestor_update_speed_restrictions >> dynamo_write >> dynamo_speed_restrictions
        ingestor_update_delivered_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics
        ingestor_update_delivered_trip_metrics_yesterday >> dynamo_write >> dynamo_delivered_trip_metrics
        ingestor_update_agg_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics_weekly
        ingestor_update_agg_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics_monthly
        ingestor_populate_delivered_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics
        ingestor_populate_agg_delivered_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics_weekly
        ingestor_populate_agg_delivered_trip_metrics >> dynamo_write >> dynamo_delivered_trip_metrics_monthly
        ingestor_update_time_predictions >> dynamo_write >> dynamo_time_predictions

        # Other
        covid_recovery_dash >> standard_edge >> github_pages

        (
            datadog
            - Edge(color="plum")
            - [
                slow_zone_lambda,
                data_dashboard_api,
                ingestor_store_new_train_runs,
                ingestor_store_yesterdays_alerts,
                ingestor_bb_store_station_status,
                ingestor_bb_store_station_info,
                ingestor_bb_calc_daily_stats,
                ingestor_update_ridership,
                ingestor_update_gtfs,
                ingestor_update_agg_trip_metrics,
                ingestor_update_speed_restrictions,
                ingestor_update_time_predictions,
                ingestor_store_landing_data,
                ingestor_populate_delivered_trip_metrics,
                ingestor_populate_agg_delivered_trip_metrics,
                ingestor_update_delivered_trip_metrics,
                ingestor_update_delivered_trip_metrics_yesterday,
            ]
        )
