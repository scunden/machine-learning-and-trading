import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt
from pandas.plotting import table 

def author():
    return "scunden3"

def EMA(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), window=50):

    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()
    df_rolling = df.ewm(span=window, adjust=False).mean()/df.ewm(span=window, adjust=False).mean()[window]
    df = df/df[0]

    return df_rolling/df - 1

def SMA(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), window=50):

    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()
    df_rolling = df.rolling(window=window).mean()
    
    return df/df_rolling 

def BB(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), window=50):
    
    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()
    df_rolling = df.rolling(window=window).mean()
    std = df.rolling(window=window).std()
    df_upper = df_rolling + std
    df_lower = df_rolling - std
    bb_value = (df - df_rolling)/(2 * std)
    
    return bb_value
    
def GoldenCrossSMA(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), window1=50, window2=200):
    symbol='JPM'
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009,12,31)

    df = get_data(["JPM"], pd.date_range(sd , ed)).loc[:,"JPM"].sort_index()
    
    df_rolling_1 = df.rolling(window=window1).mean()/df.rolling(window=window1).mean()[window1]
    df_rolling_2 = df.rolling(window=window2).mean()/df.rolling(window=window2).mean()[window2]
    df = df/df[0]

    plt.plot(df, label="Price")
    plt.plot(df_rolling_1, label="SMA({})".format(window1))
    plt.plot(df_rolling_2, label="SMA({})".format(window2))

    plt.xticks(rotation=90)
    plt.legend(loc="lower left")
    plt.grid(which='major', axis='both', linestyle='--')
    plt.title("Golden Cross with SMA({}) and SMA({})".format(window1, window2))
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.tight_layout()
    plt.plot_date(dt.datetime(2009,5,30), 0.8,'or', fillstyle='none', ms=50.0) 
    plt.savefig("Golden_Cross_SMA.png")
    plt.close()
    print("Golden Cross Completed")
    
    return df_rolling_1, df_rolling_2
    

    
def MACD(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), window1=12, window2=26, window3=9):

    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()
    
    df_rolling_1 = df.ewm(span=window1, adjust=False).mean()/df.ewm(span=window1, adjust=False).mean()[window1]
    df_rolling_2 = df.ewm(span=window2, adjust=False).mean()/df.ewm(span=window2, adjust=False).mean()[window2]
    macd = df_rolling_1-df_rolling_2
    macd = macd/macd[0]
    signal = macd.ewm(span=window3, adjust=False).mean()/macd.ewm(span=window3, adjust=False).mean()[window3]
    df = df/df[0]

    
    return macd/signal
