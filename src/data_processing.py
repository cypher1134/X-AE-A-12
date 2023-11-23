import pandas as pd
import sqlite3
from tqdm import tqdm
import time
import sys
import os
src = os.path.dirname(os.path.realpath(__file__))
root = os.path.dirname(src)
sys.path.append(src)
sys.path.append(root)
from  Machin_Learning import predict_on_database
import data_analysis

# Initialize global variables
n = 0
init_percent = 0
raw_data = None
training_model = False
graph_dict = {}

def db_thread(path, savepath="./data/raw_data.json", force_writing=False):
    """
    Load or create a JSON file with raw data from a SQLite database.

    Parameters:
    - path (str): Path to the SQLite database.
    - savepath (str): Path to save the raw data as a JSON file.
    - force_writing (bool): Force writing to JSON even if the file exists.
    """
    global raw_data
    global init_percent
    global training_model
    global graph_dict

    # Try to load raw_data from JSON file if not force_writing
    if not force_writing:
        try:
            raw_data = pd.read_json(savepath, convert_dates=False)
            graph_dict = data_analysis.graph_dict_generate(raw_data)
            print('-----Finished loading raw_data-----')
        except Exception as e:
            print(e)
            raw_data = None

    # If force_writing or raw_data is still None, read from the SQLite database
    if force_writing or raw_data is None:
        db_conn = sqlite3.connect(path)
        db_cursor = db_conn.cursor()
        raw_data = db_to_dataframe(db_cursor)
        training_model = True
        raw_data['date'] = raw_data['date'].apply(twi_time_to_unix)
        raw_data['fake_value'] = update_fake_value(raw_data)  
        raw_data['confidence'] = update_confidence(raw_data)
        raw_data = predict_on_database(raw_data)
        raw_data.to_json(savepath)
        graph_dict = data_analysis.graph_dict_generate(raw_data, True)
        training_model = False
        print('-----Raw_data registered-----')

    init_percent = 100

def db_to_dataframe(cursor):
    """
    Convert SQLite cursor data to a DataFrame.

    Parameters:
    - cursor: SQLite cursor object.

    Returns:
    - data (pd.DataFrame): DataFrame containing tweet data.
    """
    global n
    data = pd.DataFrame(columns=['id', 'user', 'text', 'view', 'like', 'retweet', 'date'])
    aide = None

    cursor.execute("SELECT Count(*) FROM tweets")
    
    n= cursor.fetchone()[0]
    # n=1000
    print("n= "+str(n))
    cursor.execute('SELECT * FROM tweets')
    global init_percent
    for i in range(n):
        
        init_percent = round(100 * i / max(n - 1,1))
        aide = cursor.fetchone()
        aide = [0 if v is None else v for v in aide]
        data.loc[i] = aide

    return data

def twi_time_to_unix(time_str):
    """
    Convert Twitter timestamp to Unix timestamp.

    Parameters:
    - time_str (str): Twitter timestamp.

    Returns:
    - float: Unix timestamp.
    """
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S+00:00"))

def update_fake_value(data):
    """
    Update the 'fake_value' column to FAKE.

    Parameters:
    - data (pd.DataFrame): DataFrame containing tweet data.

    Returns:
    - list: List of fake values.
    """
    return ['FAKE'] * len(data)
    
def update_confidence(data):
    """
    Update the 'confidence' column to 0.0.

    Parameters:
    - data (pd.DataFrame): DataFrame containing tweet data.

    Returns:
    - list: List of confidence values.
    """

    return [0.0] * len(data)