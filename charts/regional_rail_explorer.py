from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import React
from diagrams.aws.compute import EC2Instance

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")

def regional_rail_explorer():
    with Diagram("Regional Rail Explorer - Architecture", filename="diagrams/regional_rail_explorer_architecture", graph_attr=graph_attr, show=False):
        
        # application code
        with Cluster("regional-rail-explorer"):
            regional_rail_explorer = React("Regional Rail Explorer")

        # cloud resources
        with Cluster("AWS", graph_attr={"margin": "35"}):
            with Cluster("EC2"):
                ec2_rre = EC2Instance("rre-regionalrail.rocks")

        # Edges
        regional_rail_explorer >> standard_edge >> ec2_rre
