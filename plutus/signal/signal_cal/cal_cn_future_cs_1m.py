from plutus.signal.signal_cal.cal_signal_base import (
    CalSignal,
)


class CalSignalMom(CalSignal):
    def __init__(self, signalhub_dir: str = "/mnt/gitee/quanthub/signalhub/"):
        """
        计算动量因子类相应的交易信号
        :param signalhub_dir:交易信号的存放路径
        """
        super(CalSignalMom, self).__init__(signalhub_dir)
        self.drop_symbol_list = ["T", "TF", "TS", "IC", "IH", "IF", "BC", "LU", "NR"]
        self.sginal_db = "raw/cn/future/cs/1m/"
        self.sginal_tb = "mom/"

    def cal_rt_all_signal(self, factor_df_list: list):
        return self.cal_all_signal(factor_df_list)

    def cal_his_all_signal(self, factor_df_list: list):
        # factor_df2 = factor_df[~(factor_df["symbol"].isin(self.drop_symbol_list))]
        self.cal_and_save_all_signal(factor_df_list, self.sginal_db, tb=self.sginal_tb)


if __name__ == "__main__":
    cal_signal_mom = CalSignalMom()
    all_factor_df = cal_signal_mom.read_parquet(
        "/mnt/gitee/quanthub/factorhub/raw/cn/future/cs/1m/mom/",
        filters=[("symbol", "not in", cal_signal_mom.drop_symbol_list)],
    )

    factor_name_list = all_factor_df["name"].unique()
    factor_df_list = [
        all_factor_df[all_factor_df["name"] == factor_name]
        for factor_name in factor_name_list
    ]
    cal_signal_mom.cal_his_all_signal(factor_df_list)
    print("cal his mom signal ")
