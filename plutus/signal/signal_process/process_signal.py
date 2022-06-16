import pandas as pd

from plutus.signal.signal_base import SignalBase


class ProcessSignal(SignalBase):
    @staticmethod
    def aggregate_all_signal(
        signal_df: pd.DataFrame, groupby_col: list = ["trading_date", "symbol"]
    ) -> pd.DataFrame:
        """
        聚合全部因子的信号
        :param signal_df:信号数据
        :return:合并的信号
        :param groupby_col:聚合的列
        """
        signal_aggregated = signal_df.groupy(groupby_col).sum()
        return signal_aggregated
