from datetime import datetime
import pandas as pd
import plotly.express as px

def dataframe_search(df, col, search):
    """
    Searches a dataframe column for a specific string.

    Parameters:
    - df: dataframe
    - col: column name in the DataFrame
    - search: string to search for in the specified column

    Returns:
    dataframe: Subset of the original dataframe containing rows matching the search string.
    """
    if search != "":
        return df.loc[df[col].str.contains(search, case=False)]
    else:
        return df

def dataframe_count(df, col):
    """
    Returns value counts for a specified DataFrame column.

    Parameters:
    - df: dataframe
    - col: column name in the dataframe

    Returns:
    Series: value counts for the specified column.
    """
    return df[col].value_counts()

def unix_to_day(date):
    """
    Converts a Unix timestamp to a formatted date ('YYYY/MM/DD').

    Parameters:
    - date: Unix timestamp

    Returns:
    str: Formatted date string.
    """
    return datetime.utcfromtimestamp(date).strftime('%Y/%m/%d')

def dataframe_unix_to_day(df):
    """
    Converts the 'date' column in a dataframe from Unix timestamps to formatted dates.

    Parameters:
    - df: dataframe with a 'date' column containing Unix timestamps

    Returns:
    Dataframe: original dataframe with the 'date' column converted to formatted dates.
    """
    tdf = df.copy()
    tdf['date'] = tdf['date'].apply(unix_to_day)
    return tdf

def dataframe_select_period(df, begin, end):
    """
    Selects a period of data from a dataframe based on specified start and end dates.

    Parameters:
    - df: dataframe
    - begin: Start date (Unix timestamp)
    - end: End date (Unix timestamp)

    Returns:
    Dataframe: Subset of the original dataframe within the specified date range.
    """
    tdf = df.copy()
    if begin != "":
        tdf = tdf[tdf.date >= int(begin) + 3600]
    if end != "":
        tdf = tdf[tdf.date <= int(end) + 86400]
    return tdf

def FAKE_to_binary(FAKE_text):
    """
    Converts a 'FAKE' or 'true' label to binary (1 or 0).

    Parameters:
    - FAKE_text: label indicating whether a text is 'FAKE' or 'true'

    Returns:
    int: binary representation (1 for 'FAKE', 0 for 'true').
    """
    if FAKE_text == "FAKE":
        return 1
    else:
        return 0

def tweet_count_hist(df, begin="", end=""):
    """
    Returns a histogram of tweet counts per day within a specified period.

    Parameters:
    - df: dataframe
    - begin: start date (Unix timestamp)
    - end: end date (Unix timestamp)

    Returns:
    Plotly express histogram: histogram of tweet counts per day.
    """
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    tdf = dataframe_count(tdf, 'date')
    tdf = pd.DataFrame({'date':tdf.index, 'tweets':tdf.values}).sort_values(by=['date'])
    return px.histogram(tdf, x="date", y="tweets", template="darkly")

def like_retweet_view_count_line(df, begin="", end=""):
    """
    Returns line plots of 'like,' 'retweet,' and 'view' counts per day within a specified period.

    Parameters:
    - df: dataframe
    - begin: start date (Unix timestamp)
    - end: end date (Unix timestamp)

    Returns:
    tuple of plotly express line plots: Line plots for 'like,' 'retweet,' and 'view' counts per day.
    """
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    return (
        px.line(tdf.groupby('date')['like'].sum(), template="darkly"),
        px.line(tdf.groupby('date')['retweet'].sum(), template="darkly"),
        px.line(tdf.groupby('date')['view'].sum(), template="darkly")
    )

def FAKE_pie_line(df, begin="", end=""):
    """
    Returns a pie chart and line plot of the binary 'FAKE' label per day within a specified period.

    Parameters:
    - df: dataframe
    - begin: start date (Unix timestamp)
    - end: end date (Unix timestamp)

    Returns:
    tuple of plotly express pie chart and line plot: pie chart and line plot for the binary 'FAKE' label per day.
    """
    tdf = dataframe_select_period(df, begin, end)
    tdf = dataframe_unix_to_day(tdf)
    ldf = tdf.copy()
    ldf["FAKE_value"] = ldf["FAKE_value"].apply(FAKE_to_binary)
    FAKE_nb = len(tdf[tdf["FAKE_value"]=="FAKE"])
    FAKE_perc = pd.DataFrame.from_dict({
        "FAKE_perc": [FAKE_nb, len(tdf) - FAKE_nb], 
        "FAKE":['FAKE', 'true']
    })
    return (
        px.pie(FAKE_perc, values='FAKE_perc', names='FAKE', hole=.7, template="darkly", color='FAKE', color_discrete_map={
           'true':'green',
           'FAKE':'red'
        }),
        px.line(ldf.groupby('date')['FAKE_value'].sum(), template="darkly")
    )