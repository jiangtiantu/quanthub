import pandas as pd

from plutus.factor.factor_base import FactorBase


class ProcessFactor(FactorBase):
    @staticmethod
    def aggregate_all_factor(
        factor_df: pd.DataFrame, groupby_col: list = ["trading_date", "symbol"]
    ) -> pd.DataFrame:
        """
        聚合全部因子的信号
        :param factor_df:信号数据
        :return:合并的信号
        :groupby_col:聚合的列
        """
        factor_aggregated = factor_df.groupy(groupby_col).sum()
        return factor_aggregated


class ProcessFutureFactor(ProcessFactor):
    pass


class ProcessStockFactor(ProcessFactor):
    pass
