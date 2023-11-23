import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import sqlite3
import sys
import os
# Getting the name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name where the current directory is present.
root = os.path.dirname(current)
# Adding the parent directory to the sys.path.
sys.path.append(root)


connection = os.path.abspath(os.path.join(root, 'data', "scrab.db.csv"))
cursor = connection.cursor()

async def main():
    """
    Asynchronous function to scrape tweets using the twscrape library.

    Scrapes tweets related to "Xname" in Langueg: lg from dat1, to dat2,
    and stores them in a SQLite database.

    Parameters:
    None

    Returns:
    None
    """
    Xname="bill gates"
    lg="en"
    date1="2023-11-01"
    date2="2023-11-"
    api = API()
    for i in range(18,0,-1):
        q = "{Xname} lang:{lg} since:{date1} until:{date2}{}".format(i)
        async for tweet in api.search(q, limit=500):
            print(tweet.id, tweet.user.username)
            try:
                cursor.execute("SELECT Count() FROM tweets WHERE id = ?", (tweet.id,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO tweets VALUES (?, ?, ?, ?, ?, ?, ?)", (tweet.id, tweet.user.username, tweet.rawContent, tweet.viewCount, tweet.likeCount, tweet.retweetCount, tweet.date))
                    connection.commit()
                else:
                    print("already in the database")
            except:
                print("failed to write inside db")

if __name__ == "__main__":
    asyncio.run(main())
