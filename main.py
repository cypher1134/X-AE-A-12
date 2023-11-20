from src import data, dashboard
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import time

if __name__ == "__main__":
    db_conn = sqlite3.connect("data/scrap.db")
    db_cursor = db_conn.cursor()
    raw_data = data.db_to_dataframe(db_cursor)
    raw_data['date'] = raw_data['date'].apply(data.twi_time_to_unix)

    load_figure_template("darkly")
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

    app.layout = html.Div([
        dbc.Row([
            dbc.Progress(value=50, id="progressbar_init"),
            dcc.Interval(id='clock', interval=1000, n_intervals=0, max_intervals=-1),
            dbc.InputGroup([
                dbc.InputGroupText("Search"), 
                dbc.Input(id="search", type="text", placeholder="Type something...", debounce=True)
            ], className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([dash_table.DataTable(data=raw_data.to_dict('records'), page_size=10, id='table', virtualization=True)], className="dbc", width=6),
            dbc.Col([
                dcc.Graph(figure={}, id='tweet_count'),
                dcc.Graph(figure={}, id='polarity'),
                dbc.Card("This is also within a body", body=True),
            ], width=5)
        ]),
    ])
    app.run(debug = True)

    @app.callback(
    Input("clock", "n_intervals"),
    Output("progressbar_init", "value"),
    )
    def progress_bar_update(n):
        return(data.init_percent * 100,)