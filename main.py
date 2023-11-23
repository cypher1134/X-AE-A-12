from src import dashboard, data_processing
import pandas as pd
import sqlite3
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import time
from datetime import date, datetime
from threading import Thread
import parcours
import graph

def date_iso_to_unix(begin_date, end_date):
    """
    Converts ISO-formatted date strings to Unix timestamps.

    Parameters:
    - begin_date: str, ISO-formatted start date.
    - end_date: str, ISO-formatted end date.

    Returns:
    tuple: Unix timestamps for the start and end dates.
    """
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
        dbc.Collapse(dbc.Progress(value=50, id="progressbar_init", striped=False, animated=True), id="collapse_bar", is_open=False),
        dbc.Collapse(dbc.Row([
            dbc.InputGroup([
                dbc.InputGroupText("Search"), 
                dbc.Input(id="search_graph", type="text", placeholder="Select username", debounce=True)
            ], className="mb-3"),
            cyto.Cytoscape(id='cytoscape_quotes', elements=elements, style={'width': '100%', 'height': '600px', 'backgroundColor': '#91A3B0'}, layout={'name': 'cose'}, stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        "width": "data(size)",
                        "height": "data(size)",
                        "content": "data(label)",
                        "font-size": "data(font_size)",
                        "text-valign": "center",
                        "text-halign": "center",
                        "background-color": "data(fake_color)"
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'vee',
                        'target-arrow-color': 'data(color)',
                        'line-color': 'data(color)',

                    },

                },
                {
                    'selector': '[number_links <= 10]',
                    'style': {
                        "content": "",
                    }
                },
            ]),
        ])),
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
                dbc.CardHeader("Tweets per day"),
                dbc.Row(dcc.Graph(figure={}, id='tweet_count'), style={"height": "400px"}),
                dbc.CardHeader("Fake news percentage"),
                dbc.Row(dcc.Graph(figure={}, id='fake_perc'), style={"height": "300px"})
            ], width=4),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.CardHeader("Interactions stats"),
                        dbc.Row(dcc.Graph(figure={}, id='view'), style={"height": "130px"}),
                        dbc.Row(dcc.Graph(figure={}, id='retweet'), style={"height": "130px"}),
                        dbc.Row(dcc.Graph(figure={}, id='like'), style={"height": "130px"}),
                    ], className="", style={"maxHeight": "350px", "overflow": "scroll", 'max-width': '100%', 'overflow-x': 'hidden'}, width = 8),
                    dbc.Col(dbc.Row([
                        dbc.CardHeader("Fakes news per day"),
                        dcc.Graph(figure={}, id='fake_line'), 
                    ], style={"height": "350px"}, className="g-0"), className="", width = 4),
                ], style={"maxHeight": "350px"}),
                # dbc.Row([
                #     dbc.Col(dcc.Graph(figure={}, id='fakelnewsss'), className="g-0"),
                #     dbc.Col(dcc.Graph(figure={}, id='fakenews'), className="g-0"),
                # ]),
            ], width=8),
        ])),
    ], className="g-0", style={'height':'100vh'})], style={'max-width': '100%', 'overflow-x': 'hidden', 'overflow-y': 'hidden'})

    @app.callback(
        Output("progressbar_init", "value"),
        Output("progressbar_init", "label"),
        Output("progressbar_init", "striped"),
        Output("progressbar_init", "animated"),
        Output("collapse_bar", "is_open"),
        Output("clock", "max_intervals"),
        Output('tweet_count', 'figure'),
        Output('like', 'figure'),
        Output('retweet', 'figure'),
        Output('view', 'figure'),
        Output('fake_perc', 'figure'),
        Output('fake_line', 'figure'),
        Output("date-picker-range", "disabled"),
        Output("cytoscape_quotes", "elements"),
        Input("clock", "n_intervals"),
        Input('search', 'value'),
        Input('search_graph', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input("date-switch", "value"),
    )
    def progress_bar_update(n, search, search_graph, begin_date, end_date, date_switch):
        """
        Updates the progress bar and generates figures based on user input.

        Parameters:
        - n: int, interval count.
        - search: str, search string.
        - search_graph: str, search string for the graph.
        - begin_date: str, start date.
        - end_date: str, end date.
        - date_switch: list, switch state for all period.

        Returns:
        tuple: progress bar values, figures, and control settings.
        """
        date_switch_state = bool(len(date_switch))
        if data_processing.init_percent >= 100 and data_processing.training_model == False:
            collapse_bar = False
            clock_stat = 0
            df_search = dashboard.dataframe_search(data_processing.raw_data, "text", str(search or '', ))
            if date_switch_state:
                fake_perc_figure, fake_line_figure = dashboard.fake_pie_line(df_search)
                tweet_count_figure = dashboard.tweet_count_hist(df_search)
                like_count_figure, retweet_count_figure, view_count_figure  = dashboard.like_retweet_view_count_line(df_search)
            else:
                unix_begin_date, unix_end_date = date_iso_to_unix(begin_date, end_date)
                fake_perc_figure, fake_line_figure = dashboard.fake_pie_line(df_search, unix_begin_date, unix_end_date)
                tweet_count_figure = dashboard.tweet_count_hist(df_search, unix_begin_date, unix_end_date)
                like_count_figure, retweet_count_figure, view_count_figure = dashboard.like_retweet_view_count_line(df_search, unix_begin_date, unix_end_date)
            fake_perc_figure.update_layout(margin=dict(l=2, r=2, t=10, b=2))
            fake_line_figure.update_layout(margin=dict(l=2, r=2, t=10, b=2), xaxis_visible=False, xaxis_showticklabels=False, showlegend=False)
            like_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=True),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="likes", margin=dict(l=2, r=10, t=2, b=2))
            view_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="views", margin=dict(l=2, r=10, t=2, b=2))
            retweet_count_figure.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),showlegend=False, xaxis_visible=False, xaxis_showticklabels=False, yaxis_title="retweets", margin=dict(l=10, r=2, t=2, b=2))
            if search_graph is not None:
                try:
                    parcours.select_biggest_connected_graph(graph_dict, search_graph)
                    cyto_elements = graph.graph_from_dict(main_node_graph_dict)
                except:
                    cyto_elements = []
            else:
                cyto_elements = []
        else :
            collapse_bar = True
            clock_stat = -1
            fake_perc_figure, fake_line_figure = None, None
            tweet_count_figure = None
            like_count_figure, retweet_count_figure, view_count_figure = None, None, None
            cyto_elements = []
        return (
            data_processing.init_percent, 
            str(data_processing.init_percent) + ' %',
            data_processing.training_model,
            data_processing.training_model,
            collapse_bar, 
            clock_stat, 
            tweet_count_figure, 
            like_count_figure, 
            retweet_count_figure, 
            view_count_figure, 
            fake_perc_figure,
            fake_line_figure,
            date_switch_state,
            cyto_elements
        )

    @app.callback(
        Output("collapse_search", "is_open"),
        Input("tabs", "active_tab"),
    )
    def switch_tab(at):
        """
        Switches the search tab's visibility.

        Parameters:
        - at: str, active tab.

        Returns:
        bool: search tab visibility state.
        """
        if at == "tab-1":
            return False
        elif at == "tab-2":
            return True
    
    thread = Thread(target=data_processing.db_thread, args=("./data/scrap.db",))
    thread.start()
    
    app.run(debug = True)