import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import sqlite3

connection = sqlite3.connect("data/scrap.db")
cursor = connection.cursor()

async def main():
    """
    Asynchronous function to scrape tweets using the twscrape library.

    Scrapes tweets related to "bill gates" in English from November 1, 2023, to November 18, 2023,
    and stores them in a SQLite database.

    Parameters:
    None

    Returns:
    None
    """
    api = API()
    for i in range(18,0,-1):
        q = "bill gates lang:en since:2023-11-01 until:2023-11-{}".format(i)
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
