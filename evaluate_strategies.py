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
import experiment2 as exp2
import BagLearner as bl, LinRegLearner as lrl, DTLearner as dtl, RTLearner as rtl

def author():
    return "scunden3"

def normalize(df):
    return df/df[0]

def mstrat_v_benchmark(symbol="JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sample="In"):
    
    COMMISSION = 9.95
    IMPACT = 0.005
    SV = 100000
    SD = sd
    ED = ed
    SYMBOL=symbol
    
    m_trades = mstrat.testPolicy(symbol=SYMBOL,sd=SD, ed=ED,sv=SV)
    m_trades_portval =  ms.compute_portvals(m_trades, start_val=SV,commission=COMMISSION,impact=IMPACT)
    m_trades_portval = normalize(m_trades_portval)
    ls_pos = m_trades[m_trades.Shares.isin([-2000,2000])]
    
    bm_trades_portval =  mstrat.benchmarkPolicy(symbol=SYMBOL,sd=SD,ed=ED,sv = SV,commission=COMMISSION,impact=IMPACT)
    bm_trades_portval = normalize(bm_trades_portval)
    
    plt.plot(m_trades_portval, label="Manual Strategy", color='r')
    plt.plot(bm_trades_portval, label="Benchmark", color='g')
    
    first_long, first_short = 1,1
    
    for idx, value in enumerate(ls_pos.values):
        
        if value[0]>0:
            if first_long:
                plt.axvline(ls_pos.index[idx], color="blue", linestyle="--", linewidth=1, label="Long Entry")
                first_long = 0
            else:
                plt.axvline(ls_pos.index[idx], color="blue", linestyle="--", linewidth=1)
        else:
            if first_short:
                plt.axvline(ls_pos.index[idx], color="black", linestyle="--", linewidth=1, label="Short Entry")
                first_short = 0
            else:
                plt.axvline(ls_pos.index[idx], color="black", linestyle="--", linewidth=1)
    
    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    plt.grid(which='major', axis='both', linestyle='--')
    
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title("{}-Sample Manual Strategy v/s Benchmark\n".format(sample))

    plt.tight_layout()
    plt.savefig("{}SampleManualStrategyVBenchmark.png".format(sample))
    plt.close()
    
    print("{}-Sample Manual Strategy v/s Benchmark Saved".format(sample))
    
    return m_trades_portval, bm_trades_portval

def get_metrics(df):
    df = df / df.iloc[0]
    cr = df[-1]/df[0] -1
    adr = df[1:].pct_change().mean()
    sddr = df[1:].pct_change().std()
    sr = (adr/sddr)*(252**0.5)
    return "{:.4f}".format(cr), "{:.4f}".format(adr), "{:.4f}".format(sddr), "{:.4f}".format(sr)

def generate_charts_and_tables():
    
    # Chart 1: In Sample Manual v/s Benchmark
    m_trades_portval_is, bm_trades_portval_is =mstrat_v_benchmark(sample="In")
    
    # Chart 2: Out of Sample Manual v/s Benchmark
    m_trades_portval_os, bm_trades_portval_os = mstrat_v_benchmark(symbol="JPM",
                                                         sd = dt.datetime(2010,1,1), 
                                                         ed = dt.datetime(2011,12,31), 
                                                         sample="Out-of")
    
    
    # Table 1 and Table 2: In and Out of Sample Metrics
    m_trades_metrics_is = get_metrics(m_trades_portval_is)
    m_trades_metrics_os = get_metrics(m_trades_portval_os)
    bm_trades_metrics_is = get_metrics(bm_trades_portval_is)
    bm_trades_metrics_os = get_metrics(bm_trades_portval_os)

    is_metrics = pd.DataFrame({"In Sample: Manual Strategy": m_trades_metrics_is,  
                               "In Sample: Benchmark": bm_trades_metrics_is}, 
                           index=["Cummulative Return",
                                  "Avg. Daily Return",
                                  "Std. Dev of Daily Return",
                                  "Sharpe Ratio" ])

    os_metrics = pd.DataFrame({"Out-of-Sample: Manual Strategy": m_trades_metrics_os,  
                               "Out-of-Sample: Benchmark": bm_trades_metrics_os}, 
                           index=["Cummulative Return",
                                  "Avg. Daily Return",
                                  "Std. Dev of Daily Return",
                                  "Sharpe Ratio" ])
    
    
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    table(ax, is_metrics)
    plt.savefig('InSampleMetrics.png', bbox_inches='tight')
    print("In-Sample Metrics Table Saved")
    plt.close()
    
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    table(ax, os_metrics)
    plt.savefig('OutofSampleMetrics.png', bbox_inches='tight')
    print("Out-of-Sample Metrics Table Saved")
    plt.close()

if __name__ == "__main__":                                                                                            
    print("One does not simply think up a strategy")  
    # Chart 1 and Chart 2, Table 1 and Table 2
    generate_charts_and_tables()
    # Experiment 1
    exp1.run_experiment()
    # Experiment 2
    exp2.run_experiment()
    