from datetime import date

import numpy as np
import pandas as pd

from plutus.data.data_prepare.prepare_rt_redis import PrepareRT
from plutus.factor.factor_cal.cal_cn_future_cs_1d import CalMom
from plutus.factor.factor_define.cn_future_cs_1d_mom import Mom
from plutus.position.position_cal.cal_cn_future_cs_1d import CalPositionMom
from plutus.signal.signal_cal.cal_cn_future_cs_1d import CalSignalMom

# class ProcessPosition:
#     def __init__(self,):
#         pass

prepare_rt = PrepareRT()

# 获取数据
his_all_1d_main_df = pd.read_parquet(
    "/mnt/gitee/quanthub/datahub/raw/cn/future/md/main_1d_o_m.parquet"
)
his_all_1d_main_df.set_index(["trading_date", "symbol"], inplace=True)

realtime_all_1d_main_df = pd.DataFrame()

all_1d_main_df = pd.concat([his_all_1d_main_df, realtime_all_1d_main_df])
all_1d_main_df.sort_index(inplace=True)

symbol_liquidity_good = np.sign(
    all_1d_main_df[all_1d_main_df["turnover"] > 100000 * 10000]["turnover"]
).unstack()

symbol_liquidity_good_df = (
    symbol_liquidity_good[
        symbol_liquidity_good.columns.difference(
            ["T", "TF", "TS", "IC", "IH", "IF", "BC", "LU", "NR", "SC", "NR"]
        )
    ]
).stack()

all_1d_main_df = all_1d_main_df.loc[symbol_liquidity_good_df.index]
# print(all_1d_main_df)

# 计算因子
factor_mom_list = CalMom().cal_all_factor(Mom(all_1d_main_df))
# print(factor_mom_list)

# 计算信号
signal_mom_list = CalSignalMom().cal_rt_all_signal(factor_mom_list)
# print(signal_mom_list)

# 计算持仓
today_signal_mom_list = [
    signal_mom[signal_mom["trading_date"] == pd.to_datetime(date.today())]
    for signal_mom in signal_mom_list
]
print(today_signal_mom_list)

today_target_position_mom_list = [
    CalPositionMom(signal_df_list=today_signal_mom_list).cal_rt_target_position(
        account="test", money=10000 * 10000
    )
    for today_signal_mom in today_signal_mom_list
]
print(today_target_position_mom_list)

# yag.send('jiangtiantu@hotmail.com', 'trade_position',attachment_1)
