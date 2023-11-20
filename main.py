from src import data, dashboard
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import time
from datetime import date, datetime
from threading import Thread

def date_iso_to_unix(begin_date, end_date):
    if begin_date is not None:
        unix_begin_date = datetime.combine(date.fromisoformat(begin_date), datetime.min.time()).timestamp()
    else:
        unix_begin_date = ''
    if end_date is not None:
        unix_end_date = datetime.combine(date.fromisoformat(end_date), datetime.min.time()).timestamp()
    else:
        unix_end_date = ''
    return unix_begin_date, unix_end_date

if __name__ == "__main__":
    load_figure_template("darkly")
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

    app.layout = html.Div([
        dbc.Collapse(dbc.Progress(value=50, id="progressbar_init"), id="collapse_bar", is_open=False),
        dcc.Interval(id='clock', interval=1000, n_intervals=0, max_intervals=-1),
        dbc.Tabs([
            dbc.Tab(label="Graphs", tab_id="tab-1"),
            dbc.Tab(label="Search", tab_id="tab-2"),
        ], id="tabs", active_tab="tab-1"),
        dbc.Collapse([dbc.Row([
            dbc.Card("Search and adjust your parameters", body=True),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Search"), 
                    dbc.Input(id="search", type="text", placeholder="Type something...", debounce=True)
                ], className="mb-3"),
            ], width = 6, style={"margin-top": "30px"}),
            dbc.Col([
                dcc.DatePickerRange(id='date-picker-range', disabled=False, month_format='Do MMM, YY', with_portal=True),
                dbc.Checklist(options=[{"label": "all period", "value": 1}], value=[1], id="date-switch", switch=True),
            ], width = {"size": 4, "offset": 2}, align = "center", style={"margin-top": "30px"})
        ], style={"margin-top": "30px", "margin-left": "15px", "margin-right": "15px"}, justify="center")], id="collapse_search", is_open=False),
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='tweet_count'),
                ], className="dbc", width=6),
                dbc.Col([
                    dcc.Graph(figure={}, id='polarity'),
                ], className="dbc", width=6)
            ]),
        ], className="mt-3")
    ], style={'max-width': '100%', 'overflow-x': 'hidden'})

    @app.callback(
        Output("progressbar_init", "value"),
        Output("progressbar_init", "label"),
        Output("collapse_bar", "is_open"),
        Output("clock", "max_intervals"),
        Output('tweet_count', 'figure'),
        Output("date-picker-range", "disabled"),
        Input("clock", "n_intervals"),
        Input('search', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input("date-switch", "value"),
    )
    def progress_bar_update(n, search, begin_date, end_date, date_switch):
        date_switch_state = bool(len(date_switch))
        if data.init_percent == 100:
            collapse_bar = False
            clock_stat = 0
            if date_switch_state:
                tweet_count_figure = dashboard.tweet_count_hist(data.raw_data, "text", str(search or '', ))
            else:
                unix_begin_date, unix_end_date = date_iso_to_unix(begin_date, end_date)
                tweet_count_figure = dashboard.tweet_count_hist(data.raw_data, "text", str(search or '', ), unix_begin_date, unix_end_date)
        else :
            collapse_bar = True
            clock_stat = -1
            tweet_count_figure = None
        return data.init_percent, str(data.init_percent) + ' %', collapse_bar, clock_stat, tweet_count_figure, date_switch_state

    @app.callback(
        Output("collapse_search", "is_open"),
        Input("tabs", "active_tab"),
    )
    def switch_tab(at):
        if at == "tab-1":
            return False
        elif at == "tab-2":
            return True
    
    thread = Thread(target=data.db_thread, args=("./data/scrap.db",))
    thread.start()
    
    app.run(debug = True)