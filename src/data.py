import pandas as pd
import sqlite3
from tqdm import tqdm
import time


n=0
init_percent = 0
raw_data = None

def db_thread(path, savepath="./data/raw_data.json", force_writing=False):
    global raw_data
    global init_percent
    if not force_writing:
        try :
            raw_data=pd.read_json(savepath, convert_dates=False)
            print('-----Finished to load raw_data-----')
        except Exception as e:
            print(e)
            raw_data=None
    if force_writing or raw_data is None :
        db_conn = sqlite3.connect(path)
        db_cursor = db_conn.cursor()
        raw_data = db_to_dataframe(db_cursor)
        raw_data['date'] = raw_data['date'].apply(twi_time_to_unix)
        raw_data['fake_value'] = update_fake_value(raw_data)  
        raw_data.to_json(savepath)
        print('-----Raw_data registered-----')
    init_percent = 100


def db_to_dataframe(cursor):
    global n
    data=pd.DataFrame(columns=['id','user','text','view','like','retweet','date'])
    aide=None
    cursor.execute("SELECT Count() FROM tweets")
    n=cursor.fetchone()[0]
    cursor.execute('SELECT * FROM tweets')
    global init_percent
    for i in range(n):
        init_percent = round(100*i/(n-1))
        aide = cursor.fetchone()
        aide = [0 if v is None else v for v in aide]
        data.loc[i] = aide
    return  data

def twi_time_to_unix(time_str):
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))

def update_fake_value(data):
    return ['FAKE'] * len(data)