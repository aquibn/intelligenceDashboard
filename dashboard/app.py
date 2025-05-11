import sys
import os
# Add the parent directory to sys.path so we can import config.py from the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
from config import DB_URI, DB_NAME, COLLECTION_NAME
from dashboard.layout import serve_layout

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Threat Dashboard"
app.layout = serve_layout


# Connect to MongoDB
client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load threat data from the database
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    return df

# Update the bar chart showing number of threats per cluster
@app.callback(
    Output("cluster-bar-chart", "figure"),
    Input("cluster-dropdown", "value")
)
def update_cluster_bar(selected_cluster):
    df = load_data()
    counts = df["cluster"].value_counts().sort_index()
    fig = px.bar(x=counts.index, y=counts.values,
                 labels={"x": "Cluster", "y": "Threat Count"},
                 title="Threat Distribution by Cluster")
    return fig

# Update the dropdown menu options based on cluster values
@app.callback(
    Output("cluster-dropdown", "options"),
    Input("cluster-bar-chart", "figure")
)
def update_dropdown(_):
    df = load_data()
    clusters = sorted(df["cluster"].unique())
    return [{"label": f"Cluster {i}", "value": i} for i in clusters]

# Show threat list based on selected cluster
@app.callback(
    Output("threat-list", "children"),
    Input("cluster-dropdown", "value")
)
def show_threats(cluster_id):
    df = load_data()
    if cluster_id is not None:
        df = df[df["cluster"] == cluster_id]
    items = [
        html.Div([
            html.H6(f"{row['cve_id']}: {row['published']}", className="text-primary"),
            html.P(row['description'])
        ], className="border p-2 my-2")
        for _, row in df.iterrows()
    ]
    return items

# Show geographical map of threat mentions by country
@app.callback(
    Output("geo-threat-map", "figure"),
    Input("cluster-bar-chart", "figure")
)
def plot_geo_map(_):
    df = load_data()
    df["location"] = df["entities"].apply(lambda x: [e for e in x if e.istitle() and len(e) > 2])
    locations = sum(df["location"].tolist(), [])
    location_df = pd.DataFrame(locations, columns=["country"])
    map_df = location_df["country"].value_counts().reset_index()
    map_df.columns = ["country", "count"]
    fig = px.choropleth(map_df,
                        locations="country",
                        locationmode="country names",
                        color="count",
                        title="Threat Mentions by Country")
    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)

