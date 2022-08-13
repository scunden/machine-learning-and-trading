import datetime as dt                                                                                         
import random                                                                                                                                                                   
import pandas as pd                                                                                           
from util import get_data, plot_data
from indicators import SMA, MACD, BB
import ManualStrategy as mstrat
import StrategyLearner as sl
import marketsimcode as ms
import matplotlib.pyplot as plt
from pandas.plotting import table 

def author():
    return "scunden3"

def run_experiment():
    COMMISSION = 9.95
    IMPACT = 0.005
    SV = 100000
    SD = dt.datetime(2008,1,1)
    ED = dt.datetime(2009,12,31)
    SYMBOL="JPM"
    
    m_trades = mstrat.testPolicy(symbol=SYMBOL,sd=SD, ed=ED,sv=SV)
    
    m_trades_portval =  ms.compute_portvals(m_trades, start_val=SV,commission=COMMISSION,impact=IMPACT)
    m_trades_portval = m_trades_portval/m_trades_portval[0]
    
    bm_trades_portval =  mstrat.benchmarkPolicy(symbol=SYMBOL,sd=SD,ed=ED,sv = SV,commission=COMMISSION,impact=IMPACT)
    bm_trades_portval = bm_trades_portval/bm_trades_portval[0]
    
    learner = sl.StrategyLearner()
    learner.add_evidence()
    sl_trades = learner.testPolicy(sd=SD, ed=ED)
    sl_trades_portval =  ms.compute_portvals(sl_trades,start_val=SV,commission=COMMISSION,impact=IMPACT)
    sl_trades_portval = sl_trades_portval/sl_trades_portval[0]
    
    plt.plot(m_trades_portval, label="Manual Strategy", color='r')
    plt.plot(bm_trades_portval, label="Benchmark", color='g')
    plt.plot(sl_trades_portval, label="Strategy Learner", color='orange')
    
    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    plt.grid(which='major', axis='both', linestyle='--')
    
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title("Experiment 1: In Sample Portfolio Value by Strategy\n")

    plt.tight_layout()
    plt.savefig("Experiment1.png")
    plt.close()
    print("Experiment 1 Completed")
    
if __name__ == "__main__":                                                                                            
    run_experiment()      