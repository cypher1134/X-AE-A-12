from src import data
import pandas as pd
import sqlite3


if __name__ == "__main__":
    db_conn = sqlite3.connect("data/scrap.db")
    db_cursor = db_conn.cursor()
    raw_data = data.db_to_dataframe(db_cursor)
    raw_data['date'] = raw_data['date'].apply(data.twi_time_to_unix)
    print(raw_data)