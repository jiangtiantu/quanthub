from typing import Union

import empyrical as empl
import riskfolio as rp

from plutus.utils.database.database_control import DatabaseControl


class PortfolioBase(DatabaseControl):
    def __init__(self):
        super(PortfolioBase, self).__init__()

    @staticmethod
    def cal_pnl(signal_df, merge_data):
        """
        计算交易信号的pnl
        :param signal_df:信号数据
        :param merge_data:
        :return:
        """
        merge_data["signal"] = signal_df.set_index(["trading_date", "symbol"])["value"]
        merge_data.dropna(inplace=True)
        pnl_df = (merge_data["signal"] * merge_data["period"]).groupby(level=0).mean()
        return pnl_df

    def cal_all_ret(self, signal_df, ret_chg_arr):
        """
        计算每日收益率
        :param factor_df:
        :param ret_chg_arr:
        :return:
        """
        all_ret_df = signal_df.mul(ret_chg_arr, axis=0)
        return all_ret_df

    def cal_calmar_ratio(self, all_ret_df, day: Union[int, None] = None):
        """
        计算每日卡玛比率
        :param all_ret_df:
        :param day:
        :return:
        """
        if day is None:
            calmar_ratio = all_ret_df.apply(lambda x: empl.calmar_ratio(x))
            calmar_ratio.name = all_ret_df.index[-1]
        else:
            calmar_ratio = all_ret_df.rolling(day).apply(lambda x: empl.calmar_ratio(x))
        return calmar_ratio

    def cal_weight(self, returns):
        """
        滚动HRP,计算每日权重
        :param returns:
        :return:
        """
        port = rp.HCPortfolio(returns=returns)
        weight = port.optimization(
            model="HRP",
            codependence="pearson",
            rm="MV",
            rf=0,
            linkage="single",
            max_k=10,
            leaf_order=True,
        )

        w = weight["weights"]
        return w
