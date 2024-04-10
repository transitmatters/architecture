from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import React
from diagrams.custom import Custom
from diagrams.aws.compute import EC2Instance
from logos import mbta_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")

def new_train_tracker():
    with Diagram("New Train Tracker - Architecture", filename="diagrams/new_train_tracker_architecture", graph_attr=graph_attr, show=False):

        # data sources
        with Cluster("MBTA"):
            mbta_v3_api = Custom("MBTA v3 API", mbta_icon)

        # application code
        with Cluster("new-train-tracker"):
            new_train_tracker = React("New Train Tracker")

        # cloud resources
        with Cluster("AWS", graph_attr={"margin": "35"}):
            with Cluster("EC2"):
                ec2_ntt = EC2Instance("ntt-traintracker.transitmatters.org")

        # Edges
        mbta_v3_api >> standard_edge >> new_train_tracker
        new_train_tracker >> standard_edge >> ec2_ntt
