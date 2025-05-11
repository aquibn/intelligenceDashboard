import dash_bootstrap_components as dbc
from dash import html, dcc

def serve_layout():
    return dbc.Container([
        html.H1("🌐 Global Threat Intelligence Dashboard", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="cluster-bar-chart")
            ], width=6),

            dbc.Col([
                dcc.Graph(id="geo-threat-map")
            ], width=6),
        ]),

        html.Hr(),

        html.H4("📄 Clustered Threats"),
        dcc.Dropdown(id="cluster-dropdown", placeholder="Select cluster...", clearable=True),
        html.Div(id="threat-list", style={"maxHeight": "400px", "overflowY": "scroll"})
    ], fluid=True)
