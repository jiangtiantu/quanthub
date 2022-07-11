from typing import Union

import pandas as pd

from plutus.position.position_cal.cal_position_base import CalPosition


class CalStockPosition(CalPosition):
    def __init__(
        self,
        position_dir: str = "~/code/pro_quanthub/positionhub/",
        signal_df_list: Union[list, None] = None,
        rt_md_df: Union[pd.DataFrame, None] = None,
        code_info: Union[pd.DataFrame, None] = None,
    ):
        """
        计算相应因子的实际仓位
        :param position_dir:持仓文件存放路径
        :param signal_df_list:信号
        :param rt_md_df:添加实时行情后的行情数据
        :param code_info:交易品种信息
        """
        super(CalStockPosition, self).__init__(position_dir)

        self.rt_md_df = rt_md_df
        self.price = self.rt_md_df["close"]
        self.code_info = code_info

    def cal_target_position_by_weight(
        self,
        money: float,
        signal: pd.Series,
        price: pd.Series,
        weight: Union[pd.Series, None] = None,
        multiplier: int = 100,
    ):
        """
        加权计算目标仓位
        :param signal:
        :param multiplier:
        :param money:
        :param weight:
        :param price:
        :return:
        """
        if weight is None:
            weight = pd.Series(1 / signal.shape[0], index=signal.index)

        ss = ((money * weight * signal) / price / multiplier).dropna()
        target_position_s = ss.apply(lambda x: self.round_or_ceil(x)) * multiplier

        return target_position_s

    @staticmethod
    def get_stock_trade_code(contract: str, code_info: pd.DataFrame):
        pass
