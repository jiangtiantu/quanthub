# -- coding: utf-8 --
from datetime import datetime

import numpy as np
import pandas as pd

from plutus.position.position_cal.cal_cn_stock import CalStockPosition


class GenerateTradeFile(CalStockPosition):
    def __init__(self, position_dir):
        # super(GenerateTradeFile,self).__init__(position_dir)
        self.position_dir = position_dir
        self.today = datetime.today().strftime("%Y-%m-%d")

    @staticmethod
    def process_real_position(real_position_df):
        real_position_df.index = real_position_df["代码"].tolist()
        real_position_df.sort_values(by="方向")
        real_position_df["数量"] = (
            np.where(real_position_df["方向"] == 1, -1, 1) * real_position_df["数量"]
        )
        return real_position_df["数量"]

    @staticmethod
    def cal_diff_position(target_position_s, real_position_s):
        trade_ss = target_position_s.add(-1 * real_position_s, fill_value=0)
        trade_df = pd.DataFrame(columns=["代码", "市场", "数量", "相对权重", "方向"])
        trade_df["数量"] = abs(trade_ss).astype(int)
        trade_df["代码"] = trade_df.index
        trade_df["方向"] = np.where(trade_ss > 0, 0, 1)
        trade_df = trade_df[trade_df["数量"] != 0]
        trade_df.sort_values(by="方向", ascending=False, inplace=True)
        return trade_df

    def generate_trade_file(self, account, target_position_s):
        real_position_df = pd.read_csv(
            f"{self.position_dir}/real_position/{self.today}.csv", encoding="gbk"
        )

        real_position_s = self.process_real_position(real_position_df)

        trade_df = self.cal_diff_position(target_position_s, real_position_s)

        trade_df.to_csv(
            f"{self.position_dir}/trade_file/{account}_trade_{self.today}.csv",
            index=False,
            encoding="gbk",
        )
        return trade_df
