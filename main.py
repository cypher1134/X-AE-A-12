from src import data
from src import data_analysis
import pandas as pd
import sqlite3
from src import graph

if __name__ == "__main__":
    db_conn = sqlite3.connect("data/scrap.db")
    db_cursor = db_conn.cursor()
    raw_data = data.db_to_dataframe(db_cursor)
    graph_dict=data_analysis.graph_dict_generate(raw_data,True)
    print(len(graph_dict))
    raw_data['date'] = raw_data['date'].apply(data.twi_time_to_unix)
    #print(raw_data)