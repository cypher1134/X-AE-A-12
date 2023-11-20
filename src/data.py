import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from datetime import datetime


def db_to_dataframe(cursor):
    assert type(cursor)==sqlite3.Cursor,('the argument is not a cursor')
    data=pd.DataFrame(columns=['id','user','text','view','like','retweet','date'])
    aide=None
    cursor.execute("SELECT Count() FROM tweets")
    n=cursor.fetchone()[0]
    cursor.execute('SELECT * FROM tweets')
    for i in tqdm(range(n)):
        aide = cursor.fetchone()#sélectionne une ligne
        aide = cursorToList(aide) #décrire la ligne sous forme de liste
        data.loc[i] = aide
    return  data

def twi_time_to_unix(time_str):
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))
def cursorToList(aide):
    row=[]
    for i in range(7):
        try: 
            case=aide[i]
        except:
            case=None
        if i==1:#pour la colonne 'user'
            if case == None:
                row.append('unknown')#s'il n'y a rien
            else:
                row.append(aide[i])
        else:
            if case==None:#s'il n'y a rien
                row.append(0)
            else:
                row.append(aide[i])
    return row
