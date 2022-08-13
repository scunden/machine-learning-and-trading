##### """"""                                                                                            
"""MC2-P1: Market simulator.                                                                                          
                                                                                          
Copyright 2018, Georgia Institute of Technology (Georgia Tech)                                                                                            
Atlanta, Georgia 30332                                                                                            
All Rights Reserved                                                                                           
                                                                                          
Template code for CS 4646/7646                                                                                            
                                                                                          
Georgia Tech asserts copyright ownership of this template and all derivative                                                                                          
works, including solutions to the projects assigned in this course. Students                                                                                          
and other users of this template code are advised not to share it with others                                                                                         
or to make it available on publicly viewable websites including repositories                                                                                          
such as github and gitlab.  This copyright statement should not be removed                                                                                            
or edited.                                                                                            
                                                                                          
We do grant permission to share solutions privately with non-students such                                                                                            
as potential employers. However, sharing with other current or future                                                                                         
students of CS 7646 is prohibited and subject to being investigated as a                                                                                          
GT honor code violation.                                                                                          
                                                                                          
-----do not edit anything above this line---                                                                                          
                                                                                          
Student Name: Tucker Balch (replace with your name)                                                                                           
GT User ID: tb34 (replace with your User ID)                                                                                          
GT ID: 900897987 (replace with your GT ID)                                                                                            
"""                                                                                           
                                                                                          
import datetime as dt                                                                                         
import os                                                                                         
                                                                                          
import numpy as np                                                                                            
                                                                                          
import pandas as pd                                                                                           
from util import get_data, plot_data                                                                                          




def format_input(df, symbol="JPM"):
    df = df.reset_index()
    df.rename({"index":"Date"}, axis=1, inplace=True)
    df["Order"] = np.where(df["Shares"]<0,"SELL",np.nan)
    df["Order"] = np.where(df["Shares"]>0,"BUY",df["Order"])
    df["Shares"] = abs(df["Shares"])
    df["Symbol"] = symbol
    return df
    
    
def author(): 
    return 'scunden3'
                                                                                          
def get_closing_prices(orders):
    closing_prices = get_data(orders["Symbol"].unique(), pd.date_range(orders.Date.min()  , orders.Date.max()))   
    closing_prices = closing_prices.loc[:,orders["Symbol"].unique()]
    closing_prices_format = closing_prices.reset_index().rename(columns={'index': 'Date'}).melt(id_vars='Date',  
                                                                                        var_name="Symbol", 
                                                                                        value_name="Price")
    closing_prices_format['Date']= pd.to_datetime(closing_prices_format['Date'])
    
    return closing_prices, closing_prices_format

def format_orders(orders, closing_prices_format, commission):
    orders = pd.merge(orders, closing_prices_format, on=["Date","Symbol"], how="right")
    orders["Shares"] = np.where(orders["Order"]=="BUY",orders["Shares"],-orders["Shares"])
    
    
    commission_fees = orders[['Date','Order']][orders["Order"].isin(["BUY","SELL"])].groupby(['Date']).size()*commission
    buy = orders[orders.Order!="SELL"].pivot_table(index='Date', columns='Symbol', 
                                                      values=['Shares'], aggfunc="sum")
    sell = orders[orders.Order!="BUY"].pivot_table(index='Date', columns='Symbol', 
                                                        values=['Shares'], aggfunc="sum")
        
    return buy, sell, commission_fees
    
def build_portfolio(buy, sell, closing_prices, start_val, commission_fees, impact):
    portfolio = buy['Shares'].add(sell['Shares'], fill_value=0).fillna(0).cumsum()
    portfolio['Value'] = (portfolio*closing_prices).sum(axis=1)
    
    impact_buy = buy['Shares']*(1+impact)
    impact_sell = sell['Shares']*(1-impact)


    transactions = impact_buy.add(impact_sell, fill_value=0).fillna(0)
    
#     transactions['Spending'] = (transactions*closing_prices).sum(axis=1) + commission_fees
    transactions['Spending'] = (transactions*closing_prices).sum(axis=1) 
    transactions = pd.merge(transactions, commission_fees.rename('Commission'), left_index=True, 
                            right_index=True, how='left').fillna({"Commission":0})
    transactions['Spending'] = transactions['Spending'] + transactions['Commission']
    transactions["Leftover"] = transactions["Spending"] 
    
    for i, val in enumerate(transactions.iloc[:,len(transactions.columns)-1]):
        if i == 0:
            val = start_val-transactions.iloc[i,len(transactions.columns)-1]
        else:
            val = transactions.iloc[i-1,len(transactions.columns)-1]-transactions.iloc[i,len(transactions.columns)-1]
        transactions.iloc[i,len(transactions.columns)-1] = val
    
    return portfolio, transactions
    
def compute_portvals(                                                                                         
    orders,                                                                                            
    start_val=1000000,                                                                                            
    commission=9.95,                                                                                          
    impact=0.005
):  
    
    orders = format_input(orders)
    orders = orders.sort_values(['Date'])
    orders['Date']= pd.to_datetime(orders['Date'])

    closing_prices, closing_prices_format = get_closing_prices(orders)
    buy, sell, commission_fees = format_orders(orders, closing_prices_format, commission)
    portfolio, transactions = build_portfolio(buy, sell, closing_prices, start_val, commission_fees, impact)
    
    return portfolio['Value']+transactions['Leftover']     
