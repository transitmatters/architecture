from diagrams import Cluster, Diagram, Edge
from diagrams.aws.storage import S3
from diagrams.aws.compute import LambdaFunction
from diagrams.onprem.ci import GithubActions
from diagrams.custom import Custom

from logos import mbta_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")
s3_read = Edge(color="darkgreen", fontcolor="darkgreen", xlabel="s3 read", minlen="2")
s3_write = Edge(color="darkorange", fontcolor="darkorange", xlabel="s3 write")

def mbta_slow_zone_bot():
    with Diagram("MBTA Slow Zone Bot - Architecture", filename="diagrams/mbta_slow_zone_bot_architecture", graph_attr=graph_attr, show=False):
        
        # data sources
        with Cluster("MBTA"):
            mbta_performance_api = Custom("MBTA Performance API", mbta_icon)

        # application code
        with Cluster("mbta-slow-zone-bot"):
            slow_zone_bot = GithubActions("Slowzone Bot")

        # cloud resources
        with Cluster("AWS", graph_attr={"margin": "35"}):
            with Cluster("slow-zones"):
                slow_zone_lambda = LambdaFunction("SlowZonesLambda")
            with Cluster("S3"):
                data_dashboard_bucket = S3("dashboard.transitmatters.org")

        # Edges
        mbta_performance_api >> standard_edge >> slow_zone_lambda
        slow_zone_lambda >> s3_write >> data_dashboard_bucket
        data_dashboard_bucket >> s3_read >> slow_zone_bot

