import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from src import FN


n=0
init_percent = 0
raw_data = None
training_model = False

def db_thread(path, savepath="./data/raw_data.json", force_writing=False):
    global raw_data
    global init_percent
    global training_model
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
        training_model = True
        raw_data = FN.predict_on_database(raw_data)
        raw_data.to_json(savepath)
        print('-----Raw_data registered-----')
        training_model = False
    init_percent = 100


def db_to_dataframe(cursor):
    """Converts a SQL dabase, provided a cursor, into a Dataframe

    Args:
        cursor (sqlite3.Cursor): Cursor from sqlite3 which points to the scrap.db database

    Returns:
        data (pandas.Dataframe): Dataframe which corresponds to the SQL database
    """
    global n
    data=pd.DataFrame(columns=['id','user','text','view','like','retweet','date'])
    aide=None
    cursor.execute("SELECT Count() FROM tweets")
    n=cursor.fetchone()[0]
    ###################
    n=10000
    ###################
    cursor.execute('SELECT * FROM tweets')
    global init_percent
    for i in range(n):
        init_percent = round(100*i/(n-1))
        aide = cursor.fetchone()
        aide = [0 if v is None else v for v in aide]
        data.loc[i] = aide
    return  data

def twi_time_to_unix(time_str):
    """Converts twin time format to unix time format

    Args:
        time_str (str): value of database in 'time' axis in twin time format

    Returns:
        str : time in unix time format
    """
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))

def update_fake_value(data):
    return ['TRUE'] * len(data)