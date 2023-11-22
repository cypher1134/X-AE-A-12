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
        tdf = tdf[tdf.date >= int(begin) + 3600]
    if end != "":
        tdf = tdf[tdf.date <= int(end) + 86400]
    return tdf

def fake_to_binary(fake_text):
    if fake_text == "FAKE":
        return 1
    else:
        return 0

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

def fake_pie_line(df, begin="", end=""):
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    ldf = tdf.copy()
    ldf["fake_value"] = ldf["fake_value"].apply(fake_to_binary)
    fake_nb = len(tdf[tdf["fake_value"]=="FAKE"])
    fake_perc = pd.DataFrame.from_dict({
        "fake_perc": [fake_nb, len(tdf) - fake_nb], 
        "fake":['fake', 'true']
    })
    return (
        px.pie(fake_perc, values='fake_perc', names='fake', hole=.7, template="darkly", color='fake', color_discrete_map={
           'true':'green',
           'fake':'red'
        }),
        px.line(ldf.groupby('date')['fake_value'].sum(), template="darkly")
    )