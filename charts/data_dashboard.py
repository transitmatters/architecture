from diagrams import Cluster, Diagram, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.database import DynamodbTable
from diagrams.programming.framework import React
from diagrams.custom import Custom

from logos import mbta_icon, massdot_icon, box_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")
s3_read = Edge(color="darkgreen", fontcolor="darkgreen", xlabel="s3 read")
s3_write = Edge(color="darkorange", fontcolor="darkorange", xlabel="s3 write")
dynamo_read = Edge(color="olive", fontcolor="olive", xlabel="dynamo read")
dynamo_write = Edge(color="slateblue", fontcolor="slateblue", xlabel="dynamo write")

def data_dashboard():
    with Diagram("Data Dashboard - Architecture", filename="diagrams/data_dashboard_architecture", graph_attr=graph_attr, show=False):

        # data sources
        with Cluster("MBTA"):
            mbta_performance_api = Custom("MBTA Performance API", mbta_icon)
            mbta_gtfs = Custom("MBTA GTFS", mbta_icon)
            mass_dot_blue_book = Custom("MassDOT Blue Book", massdot_icon)
            mass_dot_box = Custom("MassDOT Box", box_icon)

        # application code
        with Cluster("t-performance-dash"):
            data_dashboard_api = LambdaFunction("Data Dashboard API")
            data_dashboard_frontend = React("Data Dashboard Frontend")
            data_dashboard_api - data_dashboard_frontend

        # cloud resources
        with Cluster("AWS", graph_attr={"margin": "35"}):
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

            with Cluster("S3"):
                data_dashboard_bucket = S3("dashboard.transitmatters.org")

            with Cluster("slow-zones"):
                slow_zone_lambda = LambdaFunction("SlowZonesLambda")

            with Cluster("data-ingestor"):
                ingestor_store_new_train_runs = LambdaFunction("StoreNewTrainRuns")
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


        # API Edges
        mbta_performance_api >> standard_edge >> slow_zone_lambda
        mbta_performance_api >> standard_edge >> data_dashboard_api
        mbta_performance_api >> standard_edge >> ingestor_store_new_train_runs
        mbta_gtfs >> standard_edge >> ingestor_update_gtfs
        mass_dot_blue_book >> standard_edge >> ingestor_update_speed_restrictions
        mass_dot_box >> standard_edge >> ingestor_update_ridership
        slow_zone_lambda >> s3_write >> data_dashboard_bucket
        data_dashboard_bucket >> s3_read >> data_dashboard_frontend

        # Ingestor to S3 Connections
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
