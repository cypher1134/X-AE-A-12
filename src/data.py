import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from datetime import datetime


init_percent = 0
raw_data = None

def db_thread(path):
    global raw_data
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    raw_data = db_to_dataframe(cursor)
    raw_data['date'] = raw_data['date'].apply(twi_time_to_unix)


def db_to_dataframe(cursor):
    data=pd.DataFrame(columns=['id','user','text','view','like','retweet','date'])
    aide=None
    cursor.execute("SELECT Count() FROM tweets")
    n=cursor.fetchone()[0]
    ###################################
    n=10000
    ###################################
    cursor.execute('SELECT * FROM tweets')
    global init_percent
    for i in range(n):
        init_percent = round(i/(n-1), 2)
        aide = cursor.fetchone()
        aide = [0 if v is None else v for v in aide]
        data.loc[i] = aide
    return  data

def twi_time_to_unix(time_str):
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))
    
