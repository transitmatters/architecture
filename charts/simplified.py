from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python, Typescript, Go
from diagrams.aws.storage import S3
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.database import Dynamodb, DynamodbTable
from diagrams.saas.logging import DataDog
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import React
from diagrams.custom import Custom
from diagrams.onprem.vcs import Github
from diagrams.aws.compute import EC2

from logos import mbta_icon, massdot_icon, box_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "1"}
standard_edge = Edge(minlen="3")

def simplified():
    graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "1"}
    with Diagram("TransitMatters - Simplified Architecture", filename="diagrams/transitmatters_simplified_architecture", graph_attr=graph_attr, show=False):
        with Cluster("MBTA"):
            mbta_performance_api = Custom("MBTA Performance API", mbta_icon)
            mbta_v3_api = Custom("MBTA v3 API", mbta_icon)
            mbta_gtfs = Custom("MBTA GTFS", mbta_icon)
            mbta_gtfs_rt = Custom("MBTA GTFS-RT", mbta_icon)
            mass_dot_blue_book = Custom("MassDOT Blue Book", massdot_icon)
            mass_dot_box = Custom("MassDOT Box", box_icon)

        with Cluster("TransitMatters"):
            with Cluster("t-performance-dash"):
                data_dashboard_api = LambdaFunction("Data Dashboard API")
                data_dashboard_frontend = React("Data Dashboard Frontend")
                data_dashboard_api - data_dashboard_frontend

            with Cluster("data-ingestor"):
                data_ingestors = LambdaFunction("data-ingestors")

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

        with Cluster("AWS"):
            s3 = S3("S3")
            dynamo = Dynamodb("DynamoDB")
            ec2 = EC2("EC2 VMs")

        with Cluster("GitHub"):
            github_pages = Github("GitHub Pages")

        mbta_performance_api >> standard_edge >> data_dashboard_api
        mbta_performance_api >> standard_edge >> data_ingestors
        mbta_performance_api >> standard_edge >> slow_zone_lambda
        mbta_v3_api >> standard_edge >> new_train_tracker
        mbta_gtfs >> standard_edge >> data_ingestors
        mbta_gtfs >> standard_edge >> covid_recovery_dash
        mass_dot_box >> standard_edge >> data_ingestors
        mass_dot_box >> standard_edge >> covid_recovery_dash
        mass_dot_blue_book >> standard_edge >> data_ingestors
        data_ingestors >> standard_edge >> dynamo
        data_ingestors >> standard_edge >> s3
        slow_zone_lambda >> standard_edge >> s3
        dynamo >> standard_edge >> data_dashboard_api
        s3 >> standard_edge >> data_dashboard_api
        s3 >> standard_edge >> data_dashboard_frontend
        s3 >> standard_edge >> slow_zone_bot
        covid_recovery_dash >> standard_edge >> github_pages
        new_train_tracker >> standard_edge >> ec2
        regional_rail_explorer >> standard_edge >> ec2
