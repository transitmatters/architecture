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


def simplified():
    graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "1"}
    with Diagram("Transitmatters - Architecture Overview", filename="diagrams/simplified_architecture", graph_attr=graph_attr, show=False):
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

        mbta_performance_api >> Edge(minlen="3") >> data_dashboard_api
        mbta_performance_api >> Edge(minlen="3") >> data_ingestors
        mbta_performance_api >> Edge(minlen="3") >> slow_zone_lambda
        mbta_v3_api >> Edge(minlen="3") >> new_train_tracker
        mbta_gtfs >> Edge(minlen="3") >> data_ingestors
        mass_dot_box >> Edge(minlen="3") >> data_ingestors
        mass_dot_blue_book >> Edge(minlen="3") >> data_ingestors
        data_ingestors >> Edge(minlen="3") >> dynamo
        data_ingestors >> Edge(minlen="3") >> s3
        slow_zone_lambda >> Edge(minlen="3") >> s3
        dynamo >> Edge(minlen="3") >> data_dashboard_api
        s3 >> Edge(minlen="3") >> data_dashboard_api
        s3 >> Edge(minlen="3") >> data_dashboard_frontend
        s3 >> Edge(minlen="3") >> slow_zone_bot
        covid_recovery_dash >> Edge(minlen="3") >> github_pages
        new_train_tracker >> Edge(minlen="3") >> ec2
        regional_rail_explorer >> Edge(minlen="3") >> ec2
