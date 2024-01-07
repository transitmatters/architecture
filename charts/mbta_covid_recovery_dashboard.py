from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import React
from diagrams.onprem.vcs import Github

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")

def mbta_covid_recovery_dash():
    with Diagram("MBTA Covid Recovery Dashboard - Architecture", filename="diagrams/mbta_covid_recovery_dash_architecture", graph_attr=graph_attr, show=False):

        # application code
        with Cluster("mbta-covid-recovery-dash"):
            covid_recovery_dash = React("COVID Recovery Dashboard")

        # cloud resources
        with Cluster("GitHub"):
            github_pages = Github("GitHub Pages")

        # Edges
        covid_recovery_dash >> standard_edge >> github_pages
