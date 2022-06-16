# **researchub**

这是一个投研平台,本质是jupyter lab；

我对该模块的定义是存放,我们数据分析的各类notebook文件,以及各种测试代码,相关回测逻辑,请阅读plutus.research模块；

目前有如下demo:

```ini
├─0 Build Ideas
│      quantization.emmx
│
├─1 Data
│  ├─data_collection
│  │      export_data_from_clickhouse_to_arrow.ipynb
│  │      export_data_from_clickhouse_to_parquet.ipynb
│  │      export_data_from_clickhouse_to_parquet_by_sql.ipynb
│  │      import_data_from_parquet_to_clickhouse.ipynb
│  │
│  └─data_wrangling
│      │  alter_raw_data_clickhouse.ipynb
│      │  commercial_data_to_clickhouse.ipynb
│      │  download_data_to_parquet.ipynb
│      │  drop_duplicate_data_clickhouse.ipynb
│      │  pretreat_data_to_clickhouse.ipynb
│      │  proccess_data_to_clickhouse.ipynb
├─3 Research
│  ├─cross_section_factor_analysis
│  │      cs_factor_analysis_demo.ipynb
│  
│  ├─investment_portfolio
│  │      factor_portfolio_analysis.ipynb
│  │      investment_portfolio_analysis.ipynb
│  │      signal_portfolio_analysis.ipynb
│  │
│  └─time_series_factor_analysis
│          example.ipynb
│          ts_factor_daily_demo.
│          ts_factor_min_demo.ipynb
│
└─5 Trader and Oversight

```

​	

##  单因子分析流程（供参考）

## 引入相应模块

```python
# coding: utf-8
import pandas as pd
import numpy as np
from plutus.research.backtest.backtest import BacktestCS
from plutus.utils.visualization.plot import PlotCS

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.5f' % x) 
```

## 读取数据

```python
datapath='../../../datahub/raw/cn/stock/md/all_1d.parquet'
data_bfq=pd.read_parquet(datapath)
```

## 对数据进行基本的处理

```python
open_     = data_bfq["open"].unstack()
close    = data_bfq["close"].unstack()
high    = data_bfq["high"].unstack()
low     = data_bfq["low"].unstack()
vol      = data_bfq["volume"].unstack()
amount   = data_bfq["turnover"].unstack()

#去除涨跌停,去除停牌股
# tradeable=data_bfq['amount'].apply(lambda x :1 if x>0 else np.nan)*(data_bfq['high']-data_bfq['low']).apply(lambda x :1 if x!=0 else np.nan)*chg_1_d.stack().apply(lambda x :1 if x<0.100 else np.nan)
# tradeable=tradeable.unstack()

#获取基准
# benchmark
meta_data=pd.DataFrame()
# #megedata["period"]=close.pct_change(1).shift(-1).stack()#以收盘价交易
meta_data["period"]=open_.pct_change().shift(-2).stack()#以开盘价交易
meta_data = meta_data[np.isfinite(meta_data).all(1)]
```

## 定义一个因子

```python
def factor_simple():
    factor=-1*Close.pct_change(5)
    return factor
test_factor=factor_simple()
```

## 回测输出分组记录

```python
backtest_cs= BacktestCS()
clean_factor_data= backtest_cs.backtest_cs_vector_01(meta_data,test_factor,group_num=10)
clean_factor_data
```

## 计算回测指标

```python
ret_df, sharpe_ratio, annual_return, max_down= backtest_cs.describer_02(clean_factor_data)
```

## 画出分组累计收益

```python
PlotCS.plot_group_cumsum_pnl(clean_factor_data)
```

<img src="https://pic4.zhimg.com/v2-c8f18d5d111294736a9fc7a1efb28c2b_b.png" alt="img" style="zoom:80%;" />


## 画出long-short多空收益

```python
ret_df.plot(figsize=(16, 9), title="test")
```

![img](https://pic2.zhimg.com/v2-dab49293ebec08c02e7f1971504fa779_b.png)

****

基本上你自己定义一个因子,之后就直接开始研究了。我这个框架是学习alphalens写的,因为alphalens
太慢了,所以,就自己实现了,要快些。没有做任何封装,理解起来容易些。所有曲线没有计算手续费,没有计算对冲成本。

