import unittest
import sqlite3
from sqlite3 import Error
import src.data as data

    


class DataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_conn = sqlite3.connect("data/scrap.db")
        cls.db_cursor = cls.db_conn.cursor()
        try :
            cls.test_db_conn=sqlite3.connect('memory')
        except Error as e:
            print(e)
        cls.test_db_cursor=cls.test_db_conn.cursor()
        try:
            cls.test_db_cursor.execute('CREATE TABLE tweets (id int)')
                       
        except:
            pass
        try:
            cls.test_db_cursor.execute('CREATE TABLE wrong_table_name (id INT)') 
        except:
            pass
        try:
            cls.test_db_cursor.execute('''IF (NOT EXISTS(SELECT 1 FROM tweets))
                                       BEGIN
                                            INSERT INTO tweets (id) VALUES (1),(2),(3),(5),(6);
                                        END''')
            cls.test_db_conn.commit()
        except sqlite3.Error as e:
            print(e)
        print('Finished setting up')
    @unittest.skip('Work in progress')
    def testDbToDfAssertionWrongType(cls):
        with cls.assertRaises(AssertionError):
            data.db_to_dataframe('cls.db_cursor')
            
    @unittest.skip('Work in progress')      
    def testDbToDfAssertionWrongTableName(cls):
        try:
            data.db_to_dataframe(cls.test_db_cursor.execute('SELECT * FROM wrong_table_name'))
        except sqlite3.OperationalError as e:
            print(e)
        
    
    def testDbToDfAssertionWrongTableColumn(cls):
        cls.assertEqual(data.db_to_dataframe(cls.test_db_cursor).loc[1,['user']].tolist()[0],'unknown')
           
    @classmethod
    def tearDownClass(cls):
        cls.db_conn.close()
        cls.test_db_conn.close()
        
if __name__ == '__main__':
    unittest.main()
        