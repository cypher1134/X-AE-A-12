from src import data
from src import data_analysis
from src import graph
import pandas as pd
import sqlite3
from dash import Dash
from src import graph

if __name__ == "__main__":
    force_writing=False
    if not force_writing:  
        try :
            raw_data=pd.read_json("data/raw_data.json")
            print('-----Finished to load raw_data-----')
        except Exception as e:
            print(e)
            raw_data=None
    if force_writing or raw_data.empty :
        db_conn = sqlite3.connect("data/scrap.db")
        db_cursor = db_conn.cursor()
        raw_data = data.db_to_dataframe(db_cursor)
        raw_data.to_json('data/raw_data.json')
        print('-----Raw_data registered-----')
    graph_dict=data_analysis.graph_dict_generate(raw_data.head(8000),force_writing)
    app = Dash(__name__)
    app.layout =graph.dash_graph(graph_dict)
    app.run(debug=True)
    raw_data['date'] = raw_data['date'].apply(data.twi_time_to_unix)