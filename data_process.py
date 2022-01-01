import pandas as pd


def count_article_daily_freq(df):
    # get a dataframe of frequencies
    df['date_only'] = df.Date.dt.date
    freq = df.groupby('date_only').count().Title.reset_index()
    return freq

