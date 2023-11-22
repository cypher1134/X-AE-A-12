import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from datetime import datetime

def db_to_dataframe(cursor):
    """Converts a SQL dabase, provided a cursor, into a Dataframe

    Args:
        cursor (sqlite3.Cursor): Cursor from sqlite3 which points to the scrap.db database

    Returns:
        data (pandas.Dataframe): Dataframe which corresponds to the SQL database
    """
    assert type(cursor)==sqlite3.Cursor,('the argument is not a cursor')
    columns=['id','user','text','view','like','retweet','date','fake_value']
    data=pd.DataFrame(columns=['id','user','text','view','like','retweet','date','fake_value'])
    aide=None
    cursor.execute("SELECT Count() FROM tweets")
    n = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM tweets')
    print('-----Starting conversion-----')
    for i in tqdm(range(n)):
        aide = cursor.fetchone()#sélectionne une ligne
        aide = cursorToList(aide,columns) #décrire la ligne sous forme de liste
        data.loc[i]=aide
    print('-----Finished conversion-----')
    return  data

def twi_time_to_unix(time_str):
    """Converts twin time format to unix time format

    Args:
        time_str (str): value of database in 'time' axis in twin time format

    Returns:
        str : time in unix time format
    """
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))
    

def cursorToList(aide,colums):
    if len(aide)==len(colums):
        return [e if e!=None else 0 for e in aide]
    else:
        row=[]
        for i in range(len(colums)):
            try: 
                case=aide[i]
            except:
                case=None
            if case==None:#s'il n'y a rien
                row.append(0)
            else:
                row.append(aide[i])
        return row