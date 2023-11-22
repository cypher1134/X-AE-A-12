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

    app.layout = html.Div([dbc.Card([
        dbc.Collapse(dbc.Progress(value=50, id="progressbar_init"), id="collapse_bar", is_open=False),
        dcc.Interval(id='clock', interval=1000, n_intervals=0, max_intervals=-1),
        dbc.Tabs([
            dbc.Tab(label="Graphs", tab_id="tab-1"),
            dbc.Tab(label="Search", tab_id="tab-2"),
        ], id="tabs", active_tab="tab-1"),
        dbc.Collapse([dbc.Row([
            dbc.Alert("Search and adjust your parameters", color="secondary"),
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
        dbc.CardBody(dbc.Row([
            dbc.Col([
                dbc.CardHeader("General informations"),
                dbc.Row(dcc.Graph(figure={}, id='tweet_count'), style={"height": "400px"}),
            ], width=4),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.CardHeader("Interactions stats"),
                        dbc.Row(dcc.Graph(figure={}, id='view'), style={"height": "130px"}),
                        dbc.Row(dcc.Graph(figure={}, id='retweet'), style={"height": "130px"}),
                        dbc.Row(dcc.Graph(figure={}, id='like'), style={"height": "130px"}),
                    ], className="g-0", style={"maxHeight": "350px", "overflow": "scroll", 'max-width': '100%', 'overflow-x': 'hidden'}, width = 8),
                    dbc.Col(dcc.Graph(figure={}, id='share'), className="g-0", width = 4),
                ], style={"maxHeight": "350px"}),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure={}, id='fakelnewsss'), className="g-0"),
                    dbc.Col(dcc.Graph(figure={}, id='fakenews'), className="g-0"),
                ]),
            ], width=8),
        ])),
    ], className="g-0", style={'height':'100vh'})], style={'max-width': '100%', 'overflow-x': 'hidden'})

    @app.callback(
        Output("progressbar_init", "value"),
        Output("progressbar_init", "label"),
        Output("collapse_bar", "is_open"),
        Output("clock", "max_intervals"),
        Output('tweet_count', 'figure'),
        Output('like', 'figure'),
        Output('retweet', 'figure'),
        Output('view', 'figure'),
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
            df_search = dashboard.dataframe_search(data.raw_data, "text", str(search or '', ))
            if date_switch_state:
                tweet_count_figure = dashboard.tweet_count_hist(df_search)
                like_count_figure, retweet_count_figure, view_count_figure  = dashboard.like_retweet_view_count_line(df_search)
            else:
                unix_begin_date, unix_end_date = date_iso_to_unix(begin_date, end_date)
                tweet_count_figure = dashboard.tweet_count_hist(df_search, unix_begin_date, unix_end_date)
                like_count_figure, retweet_count_figure, view_count_figure = dashboard.like_retweet_view_count_line(df_search, unix_begin_date, unix_end_date)
            like_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=True),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="likes", margin=dict(l=2, r=10, t=2, b=2))
            view_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="views", margin=dict(l=2, r=10, t=2, b=2))
            retweet_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="retweets", margin=dict(l=10, r=2, t=2, b=2))
        else :
            collapse_bar = True
            clock_stat = -1
            tweet_count_figure = None
            like_count_figure, retweet_count_figure, view_count_figure = None, None, None
        return (
            data.init_percent, 
            str(data.init_percent) + ' %', 
            collapse_bar, 
            clock_stat, 
            tweet_count_figure, 
            like_count_figure, 
            retweet_count_figure, 
            view_count_figure, 
            date_switch_state
        )

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