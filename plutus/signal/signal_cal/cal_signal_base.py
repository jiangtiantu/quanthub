import pandas as pd

from plutus.signal.signal_base import SignalBase


class CalSignal(SignalBase):
    def __init__(self, signalhub_dir: str):
        """
        计算交易信号的基类
        :param signalhub_dir:交易信号的存放地址
        """
        super(CalSignal, self).__init__(signalhub_dir)


class CalCS(CalSignal):
    def __init__(self, signalhub_dir: str):
        super(CalCS, self).__init__(signalhub_dir)

    def cal_and_save_all_signal(
        self,
        factor_df_list: list,
        db: str,
        tb: str,
        hold_num: int = 1,
    ):
        """
        计算全部信号,并存放到相应路径
        :param factor_df_list:因子数据 的列表
        :param db:数据库名
        :param tb:表名
        :param hold_num:持有hold_num组
        :return:
        """
        for factor_df in factor_df_list:
            signal_df = self.cal_signal_01(factor_df, hold_num)
            print(f"{tb}{factor_df['name'][0]}/")
            self.save_parquet(
                signal_df,
                data_dir=self.signalhub_dir,
                db=db,
                tb=f"{tb}{factor_df['name'][0]}/",
            )

    def cal_all_signal(self, factor_df_list: list, hold_num=1) -> list:
        """
        计算因子全部相应交易信号
        :param factor_df_list:因子数据 的列表
        :param hold_num:持有hold_num组
        :return:
        """
        signal_df_list = [
            self.cal_signal_01(factor_df, hold_num) for factor_df in factor_df_list
        ]
        return signal_df_list

    def cal_signal_01(
        self,
        factor_df: pd.DataFrame,
        hold_num: int,
    ) -> pd.DataFrame:
        """
        将因子数据计算为交易信号
        :param factor_df:因子数据,index为[trading_date,code] 或者[trading_date,symbol]
        :param hold_num:持有hold_num组
        :return:
        """
        input_factor_df = factor_df["value"]
        input_factor_quantile = input_factor_df.groupby(["trading_date"]).apply(
            lambda x: x.rank(method="first")
        )

        long_s = input_factor_quantile.groupby(level=0).apply(
            lambda x: x[x >= x.max() - (hold_num - 1)].droplevel(0)
        )
        long_s.iloc[:] = 1
        long_signal_s = long_s

        short_s = input_factor_quantile[input_factor_quantile <= hold_num]
        short_s.iloc[:] = -1
        short_signal_s = short_s

        signal_s = long_signal_s.add(short_signal_s, fill_value=0)
        signal_df = signal_s.reset_index()
        signal_df["name"] = factor_df["name"].unique()[0]
        signal_df["type"] = factor_df["type"].unique()[0]

        return signal_df


class CalTS(CalSignal):
    def __init__(self, signalhub_dir: str):
        super(CalTS, self).__init__(signalhub_dir)
