"""                                                                                                                                                                                                                         
Student Name: Steven Cunden                                                                                          
GT User ID: scunden3                                                                                         
GT ID: 903657919                                                                                          
"""                                                                                           
                                                                                          
import datetime as dt    
import random                                                                                                                                                                   
import pandas as pd                                                                                           
from util import get_data, plot_data
from indicators import SMA, MACD, BB
import marketsimcode as ms
import matplotlib.pyplot as plt

# The in-sample period is January 1, 2008 to December 31, 2009. 
# The out-of-sample/testing period is January 1, 2010 to December 31, 2011. 

def author():
    return "scunden3"

def optimal_purchases(current, order):
    if order == "BUY":
        if current == 1000:
            return 0
        elif current == -1000:
            return 2000
        elif current == 0:
            return 1000
        
    elif order == "SELL":
        if current == 1000:
            return -2000
        elif current == -1000:
            return 0
        elif current == 0:
            return -1000
        
def sma_signal(sma, today):
    sma_today = sma.loc[today]
    
    if sma_today < 0.6:
        return 1
    elif sma_today > 1:
        return -1
    else:
        return 0
    
def macd_signal(macd_signal_ratio, today):
    
    macd_signal_ratio = macd_signal_ratio.loc[today]
    
    if macd_signal_ratio > 1:
        return -1
        
    elif macd_signal_ratio < 1:
        return 1
    else:
        return 0
    
def bb_signal(bb, today):
    bb_today = bb.loc[today]
    
    if bb_today > 0.8:
        return -1
    elif bb_today < 0.2:
        return 1
    else:
        return 0
                                                                                      
def testPolicy(                                                                                           
    symbol="IBM",                                                                                         
    sd=dt.datetime(2008,1,1),                                                                                           
    ed=dt.datetime(2009,12,31),                                                                                           
    sv=10000,                                                                                         
):                                                                                            

    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()   
    df = df/df[0]
    psma = SMA(symbol, sd, ed, window=21)
    bb = BB(symbol, sd, ed, window=21)
    macd_signal_ratio = MACD(symbol, sd, ed, window1=12, window2=26, window3=9)
    
    current = 0
    orders = []
    last_trade_date = sd
    
    for i in df.index:
        
        sma_vote = sma_signal(psma, i)
        macd_vote = macd_signal(macd_signal_ratio, i)
        bb_vote = bb_signal(bb, i)
        

        
        votes = [sma_vote , macd_vote , bb_vote]

    
        trade_freq = i -  last_trade_date
        
    
        if trade_freq.days <= 3:
            order = 0
    
        elif len(set(votes)) ==3 or max(set(votes), key = votes.count)==0:
            order = 0
        elif max(set(votes), key = votes.count)==1:
            order = optimal_purchases(current, "BUY")
            last_trade_date = i
                
        else: 
            order = optimal_purchases(current, "SELL")
            last_trade_date = i
        
#         votes = sma_vote + macd_vote + bb_vote
#         if votes >= 2:
#             order = optimal_purchases(current, "BUY")
#         elif votes <= -1:
#             order = optimal_purchases(current, "SELL")
#         else:
#             order = 0

#         print("SMA: {} | MACD: {} | BB: {} | Final: {}".format(sma_vote, macd_vote, bb_vote, votes))    
        orders.append(order)
        current += order
            
    orders = pd.DataFrame({'Shares': orders}, index=df.index)
    return orders

def benchmarkPolicy(symbol='JPM', 
                    sd=dt.datetime(2008,1,1),
                    ed=dt.datetime(2009,12,31),  
                    sv = 100000,
                    commission=0,
                    impact=0):
    df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index()
    orders = []

    for idx, price in enumerate(df):
        if idx == 0:
            orders.append(1000)
        elif  idx < df.shape[0]-1:
            orders.append(0)

    orders = pd.DataFrame({'Shares': orders}, index=df.index[:-1])
    
    return ms.compute_portvals(orders, start_val=sv,commission=0,impact=0)