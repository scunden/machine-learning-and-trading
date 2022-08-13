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
import experiment1 as exp1
import BagLearner as bl, LinRegLearner as lrl, DTLearner as dtl, RTLearner as rtl

def author():
    return "scunden3"

def get_metrics(df):
    df = df / df.iloc[0]
    cr = df[-1]/df[0] -1
    adr = df[1:].pct_change().mean()
    sddr = df[1:].pct_change().std()
    sr = (adr/sddr)*(252**0.5)
    return "{:.4f}".format(cr), "{:.4f}".format(adr), "{:.4f}".format(sddr), "{:.4f}".format(sr)


def run_experiment():
    
    COMMISSION = 0
    SV = 100000
    SD = dt.datetime(2008,1,1)
    ED = dt.datetime(2009,12,31)
    SYMBOL="JPM"
    
    portvals = []
    impact_ls = [0, 0.005, 0.01, 0.015]
    trade_tracker = []
    
    for IMPACT in impact_ls:
        learner = sl.StrategyLearner()
        learner.add_evidence()
        sl_trades = learner.testPolicy(sd=SD, ed=ED)
        sl_trades_portval =  ms.compute_portvals(sl_trades,start_val=SV,commission=COMMISSION,impact=IMPACT)
        sl_trades_portval = sl_trades_portval/sl_trades_portval[0]
        
        plt.plot(sl_trades_portval, label="Impact {}".format(IMPACT))
        portvals.append(sl_trades_portval)
        trade_tracker.append(len(sl_trades[sl_trades["Shares"].isin([-2000,2000])].index))

    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    plt.grid(which='major', axis='both', linestyle='--')

    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title("Experiment 2: Strategy Learner In Sample Portfolio Value by Impact\n")

    plt.tight_layout()
    plt.savefig("Experiment2.png")
    plt.close()
    
    is_metrics = pd.DataFrame({
        "Impact {}".format(impact_ls[0]): get_metrics(portvals[0]),  
        "Impact {}".format(impact_ls[1]): get_metrics(portvals[1]),
        "Impact {}".format(impact_ls[2]): get_metrics(portvals[2]),
        "Impact {}".format(impact_ls[3]): get_metrics(portvals[3]),
        
    }, 
                           index=["Cummulative Return",
                                  "Avg. Daily Return",
                                  "Std. Dev of Daily Return",
                                  "Sharpe Ratio" ])
    
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    table(ax, is_metrics)
    plt.savefig('InSampleMetricsByImpact.png', bbox_inches='tight')
    plt.close()
    print("In-Sample Metrics by Impact Table Saved")

    plt.bar([str(x) for x in impact_ls], trade_tracker)
    plt.title('Number of Trades by Impact')
    plt.xlabel('Impact Size')
    plt.ylabel('Number of Trades')
    plt.savefig('TradeTable.png', bbox_inches='tight')
    plt.close()
    print("Trade Table Saved")
    
if __name__ == "__main__":                                                                                            
    run_experiment()      