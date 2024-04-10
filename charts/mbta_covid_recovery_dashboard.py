from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import React
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom
from logos import mbta_icon, massdot_icon, box_icon

# global graph attributes
graph_attr = {"beautify": "true", "concentrate": "true", "layout": "dot", "ranksep": "3"}
standard_edge = Edge(minlen="2")

def mbta_covid_recovery_dash():
    with Diagram("MBTA Covid Recovery Dashboard - Architecture", filename="diagrams/mbta_covid_recovery_dash_architecture", graph_attr=graph_attr, show=False):

        # data sources
        with Cluster("MBTA"):
            mbta_gtfs = Custom("MBTA GTFS", mbta_icon)
            mass_dot_box = Custom("MassDOT Box", box_icon)
            
        # application code
        with Cluster("mbta-covid-recovery-dash"):
            covid_recovery_dash = React("COVID Recovery Dashboard")

        # cloud resources
        with Cluster("GitHub"):
            github_pages = Github("GitHub Pages")

        # Edges
        mbta_gtfs >> standard_edge >> covid_recovery_dash
        mass_dot_box >> standard_edge >> covid_recovery_dash
        covid_recovery_dash >> standard_edge >> github_pages
