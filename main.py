from src import data, dashboard
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import time
from threading import Thread

if __name__ == "__main__":
    load_figure_template("darkly")
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css" #### MAKE IT LOCAL
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

    app.layout = html.Div([
        dbc.Row([
            dbc.Collapse(dbc.Progress(value=50, id="progressbar_init"), id="collapse_bar", is_open=False),
            dcc.Interval(id='clock', interval=1000, n_intervals=0, max_intervals=-1),
            dbc.InputGroup([
                dbc.InputGroupText("Search"), 
                dbc.Input(id="search", type="text", placeholder="Type something...", debounce=True)
            ], className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([dash_table.DataTable(page_size=10, id='table', virtualization=True)], className="dbc", width=6),
            dbc.Col([
                dcc.Graph(figure={}, id='tweet_count'),
                dcc.Graph(figure={}, id='polarity'),
                dbc.Card("This is also within a body", body=True),
            ], width=5)
        ]),
    ])

    @app.callback(
    Output("progressbar_init", "value"),
    Output("progressbar_init", "label"),
    Output("table", "data"),
    Output("collapse_bar", "is_open"),
    Input("clock", "n_intervals"),
    )
    def progress_bar_update(n):
        if data.init_percent == 1:
            dash_table_data = data.raw_data.to_dict('records')
            collapse_bar = False
        else :
            dash_table_data = None
            collapse_bar = True
        return data.init_percent * 100, str(round(data.init_percent * 100)) + ' %', dash_table_data, collapse_bar
    
    thread = Thread(target=data.db_thread, args=("./data/scrap.db",))
    thread.start()

    app.run(debug = True)