"""
Description: 
Version: 2.0
Author: your name
Date: 2022-04-17 18:48:14
LastEditTime: 2022-04-18 13:20:22
LastEditors: your name
FilePath: /quanthub/plutus/signal/signal_cal/cal_cn_stock_cs_1d.py
可以输入预定的版权声明、个性签名、空行等
"""
from plutus.signal.signal_cal.cal_signal_base import CalCS


class CalSignalMom(CalCS):
    def __init__(self, signalhub_dir: str = "/mnt/gitee/quanthub/signalhub/"):
        """
        计算动量因子类相应的交易信号
        :param signalhub_dir:交易信号的存放路径
        """
        super(CalSignalMom, self).__init__(signalhub_dir)
        self.stock_list = ["600000"]
        self.sginal_db = "raw/cn/stock/cs/1d/"
        self.sginal_tb = "mom/"

    def cal_rt_all_signal(self, factor_df_list: list, hold_num=20):
        return self.cal_all_signal(factor_df_list, hold_num=hold_num)

    def cal_his_all_signal(self, factor_df_list: list, hold_num=20):
        self.cal_and_save_all_signal(
            factor_df_list, self.sginal_db, tb=self.sginal_tb, hold_num=hold_num
        )


if __name__ == "__main__":
    cal_signal_mom = CalSignalMom()
    all_factor_df = cal_signal_mom.read_parquet(
        data_dir="/mnt/gitee/quanthub/factorhub/",
        db="raw/cn/stock/cs/1d/",
        tb="mom/",
        filters=[("code", "not in", cal_signal_mom.stock_list)],
    )
    all_factor_df.set_index(["trading_date", "code"], inplace=True)
    factor_name_list = all_factor_df["name"].unique()
    factor_df_list = [
        all_factor_df[all_factor_df["name"] == factor_name]
        for factor_name in factor_name_list
    ]
    cal_signal_mom.cal_his_all_signal(factor_df_list, hold_num=10)
    print("cal his mom signal ")
