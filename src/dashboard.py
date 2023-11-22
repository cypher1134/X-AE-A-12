from datetime import datetime
import pandas as pd
import plotly.express as px

def dataframe_search(df, col, search):
    if search != "":
        return df.loc[df[col].str.contains(search, case=False)]
    else:
        return df

def dataframe_count(df, col):
    return df[col].value_counts()

def unix_to_day(date):
    return datetime.utcfromtimestamp(date).strftime('%Y/%m/%d')

def dataframe_unix_to_day(df):
    tdf = df.copy()
    tdf['date'] = tdf['date'].apply(unix_to_day)
    return tdf

def dataframe_select_period(df, begin, end):
    tdf = df.copy()
    if begin != "":
        tdf = tdf[tdf.date >= int(begin)]
    if end != "":
        tdf = tdf[tdf.date <= int(end)]
    return tdf

def tweet_count_hist(df, begin="", end=""):
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    tdf = dataframe_count(tdf, 'date')
    tdf = pd.DataFrame({'date':tdf.index, 'tweets':tdf.values}).sort_values(by=['date'])
    return px.histogram(tdf, x="date", y="tweets", template="darkly")

def like_retweet_view_count_line(df, begin="", end=""):
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    return (
        px.line(tdf.groupby('date')['like'].sum(), template="darkly"),
        px.line(tdf.groupby('date')['retweet'].sum(), template="darkly"),
        px.line(tdf.groupby('date')['view'].sum(), template="darkly")
    )