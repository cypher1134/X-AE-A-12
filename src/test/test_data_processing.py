import pytest
import pandas as pd
import sqlite3
import time
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
src = os.path.dirname(current)
root = os.path.dirname(src)
sys.path.append(src)# parent directory to the sys.path.
sys.path.append(root)
from  data_processing import * 

# Mocking the sqlite3 connect method
class MockSQLiteCursor:
    def __init__(self):
        self.query_results = None

    def execute(self, query):
        pass

    def fetchone(self):
        # Simulate the behavior of fetchone based on your needs
        return self.query_results

    def set_query_results(self, results):
        self.query_results = results

def test_db_to_dataframe():
    db_path =  os.path.abspath(os.path.join(root, 'data', "scrap.db"))#Absolute path to the database file for the gitlab CI

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Fetch the actual number of rows in the table
    cursor.execute("SELECT COUNT(*) FROM tweets") 
    actual_num_rows = cursor.fetchone()[0]

    # Execute a SELECT query to fetch data
    cursor.execute("SELECT * FROM tweets")  
    query_results = cursor.fetchall()

    # Ensure the function returns a DataFrame
    result = db_to_dataframe(cursor)

    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check if the DataFrame has the expected columns
    expected_columns = ['id', 'user', 'text', 'view', 'like', 'retweet', 'date']
    assert result.columns.tolist() == expected_columns

    # Check if the DataFrame has the expected number of rows
    assert len(result) == actual_num_rows

    # Close the connection
    connection.close()

def test_twi_time_to_unix():
    # Test with a known Twitter timestamp
    time_str = "2023-01-01 12:00:00+00:00"
    result =  twi_time_to_unix(time_str)
    assert result != None


def test_update_fake_value():
    # Mock DataFrame
    data = pd.DataFrame({'id': [1, 2, 3], 'user': ['user1', 'user2', 'user3'], 'text': ['text1', 'text2', 'text3']})

    # Ensure the function returns a list of the same length as the DataFrame
    result =  update_fake_value(data)
    assert len(result) == len(data)

def test_update_confidence():
    # Mock DataFrame
    data = pd.DataFrame({'id': [1, 2, 3], 'user': ['user1', 'user2', 'user3'], 'text': ['text1', 'text2', 'text3']})

    # Ensure the function returns a list of the same length as the DataFrame
    result =  update_confidence(data)
    assert len(result) == len(data)
