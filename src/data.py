import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from datetime import datetime


def db_to_dataframe(cursor):
    data = pd.DataFrame(
        columns=['id', 'user', 'text', 'view', 'like', 'retweet', 'date'])
    aide = None
    cursor.execute("SELECT Count() FROM tweets")
    n = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM tweets')
    for i in tqdm(range(n)):
        aide = cursor.fetchone()
        aide = [0 if v is None else v for v in aide]
        data.loc[i] = aide
    return data


def twi_time_to_unix(time_str):
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))
