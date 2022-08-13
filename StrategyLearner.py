""""""                                                                                            
"""                                                                                           
Template for implementing StrategyLearner  (c) 2016 Tucker Balch                                                                                          
                                                                                          
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
                                                                                          
Student Name: Steven Cunden                                                                                          
GT User ID: scunden3                                                                                         
GT ID: 903657919                                                                                           
"""                                                                                           
                                                                                          
import datetime as dt  
from datetime import datetime, timedelta 
import random                                                                                       
import pandas as pd                                                                                           
from util import get_data, plot_data
import BagLearner as bl, LinRegLearner as lrl, DTLearner as dtl, RTLearner as rtl
from indicators import SMA, MACD, BB
import numpy as np
import marketsimcode as ms
                                                                                          
class StrategyLearner(object):                                                                                            
    """                                                                                           
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.                                                                                          
                                                                                          
    :param verbose: If “verbose” is True, your code can print out information for debugging.                                                                                          
        If verbose = False your code should not generate ANY output.                                                                                          
    :type verbose: bool                                                                                           
    :param impact: The market impact of each transaction, defaults to 0.0                                                                                         
    :type impact: float                                                                                           
    :param commission: The commission amount charged, defaults to 0.0                                                                                         
    :type commission: float                                                                                           
    """                                                                                           
    # constructor                                                                                         
    def __init__(self, verbose=False, impact=0.0, commission=0.0):                                                                                            
        """                                                                                           
        Constructor method                                                                                            
        """                                                                                           
        self.verbose = verbose                                                                                            
        self.impact = impact                                                                                          
        self.commission = commission    
        self.learner =  bl.BagLearner(learner = dtl.DTLearner, 
                                 kwargs = {"leaf_size":5}, 
                                 bags = 25, 
                                 boost = False, 
                                 verbose = False) 
        
    def author(self):
        print("scunden3")
        
    def optimal_purchases(self, current, order):
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
                                                                                          
    # this method should create a QLearner, and train it for trading                                                                                          
    def add_evidence(                                                                                         
        self,                                                                                         
        symbol="JPM",                                                                                         
        sd=dt.datetime(2008, 1, 1),                                                                                           
        ed=dt.datetime(2009, 12, 31),                                                                                           
        sv=10000,                                                                                         
    ):                                                                                            
        """                                                                                           
        Trains your strategy learner over a given time frame.                                                                                         
                                                                                          
        :param symbol: The stock symbol to train on                                                                                           
        :type symbol: str                                                                                         
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008                                                                                         
        :type sd: datetime                                                                                            
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009                                                                                           
        :type ed: datetime                                                                                            
        :param sv: The starting value of the portfolio                                                                                            
        :type sv: int                                                                                         
        """                                                                                           
                                                                                          
        df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index() 
        psma = SMA(symbol, sd, ed, window=15)
        bb = BB(symbol, sd, ed, window=15)
        macd_signal_ratio = MACD(symbol, sd, ed, window1=12, window2=26, window3=9)
        
        indicators_df = pd.concat((psma, bb, macd_signal_ratio/macd_signal_ratio[0]), axis=1)
        indicators_df.columns = ['PSMA', 'BB', 'MACD_SR']
        indicators_df.fillna(0, inplace=True)
        
        N_days = 10
        Xtrain = indicators_df[:-N_days].values
        Ytrain = np.zeros(Xtrain.shape[0])  # This will be based on N day Future return
        YBUY = (0.015 + self.impact)
        YSELL = (-0.015 - self.impact)
        
        for idx, i in enumerate(df[:-N_days].index):
            
            ret = (df[idx + N_days] / df[idx]) - 1.0

            if ret > YBUY:
                Ytrain[idx] = 1

            elif ret < YSELL:
                Ytrain[idx] = -1

            else:
                Ytrain[idx] = 0

        self.learner.add_evidence(Xtrain, Ytrain)
                                                                                          
    # this method should use the existing policy and test it against new data                                                                                         
    def testPolicy(                                                                                           
        self,                                                                                         
        symbol="JPM",                                                                                         
        sd=dt.datetime(2009, 1, 1),                                                                                           
        ed=dt.datetime(2010, 12, 31),                                                                                           
        sv=10000,                                                                                         
    ):                                                                                            
        """                                                                                           
        Tests your learner using data outside of the training data                                                                                            
                                                                                          
        :param symbol: The stock symbol that you trained on on                                                                                            
        :type symbol: str                                                                                         
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008                                                                                         
        :type sd: datetime                                                                                            
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009                                                                                           
        :type ed: datetime                                                                                            
        :param sv: The starting value of the portfolio                                                                                            
        :type sv: int                                                                                         
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating                                                                                            
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.                                                                                           
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to                                                                                         
            long so long as net holdings are constrained to -1000, 0, and 1000.                                                                                           
        :rtype: pandas.DataFrame                                                                                          
        """                                                                                           
                                                                                          
        df = get_data([symbol], pd.date_range(sd , ed)).loc[:,symbol].sort_index() 
        psma = SMA(symbol, sd, ed, window=15)
        bb = BB(symbol, sd, ed, window=15)
        macd_signal_ratio = MACD(symbol, sd, ed, window1=12, window2=26, window3=9)
        
        indicators_df = pd.concat((psma, bb, macd_signal_ratio/macd_signal_ratio[0]), axis=1)
        indicators_df.columns = ['PSMA', 'BB', 'MACD_SR']
        indicators_df.fillna(0, inplace=True)
        
        X_test = indicators_df.values
        Y_test = self.learner.query(X_test)
        
        current = 0
        orders = []
        
        for i in Y_test:
            
            if i==1:
                order = self.optimal_purchases(current, "BUY")
            elif i==-1:
                order = self.optimal_purchases(current, "SELL")
            else:
                order = 0

            orders.append(order)
            current += order
        
        return pd.DataFrame({"Shares": orders}, index=df.index)
    
if __name__ == "__main__":                                                                                            
    print("One does not simply think up a strategy")                                                                                          
