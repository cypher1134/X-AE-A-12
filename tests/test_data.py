import unittest
import sqlite3
import src.data as data



class DataTest(unittest.TestCase):
    def setUp(self):
        self.db_conn = sqlite3.connect("data/scrap.db")
        self.db_cursor = self.db_conn.cursor()
        print(type(self.db_cursor))
    def test_data(self):
        data.db_to_dataframe(self.db_cursor)
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()