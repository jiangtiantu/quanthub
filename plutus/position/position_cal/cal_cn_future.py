from typing import Union

import pandas as pd

from plutus.position.position_cal.cal_position_base import CalPosition


class CalPositionMom(CalPosition):
    def __init__(
        self,
        position_dir: str = "~/code/pro_quanthub/positionhub/",
        signal_df_list: Union[list, None] = None,
        rt_md_df: Union[pd.DataFrame, None] = None,
        symbol_info: Union[pd.DataFrame, None] = None,
    ):
        """
        计算相应因子的实际仓位
        :param position_dir:持仓文件存放路径
        :param signal_df_list:信号
        :param rt_md_df:添加实时行情后的行情数据
        :param symbol_info:交易品种信息
        """
        super(CalPositionMom, self).__init__(position_dir)
        self.position_db = "raw_cn_future_cs_1d"
        self.tb = "mom"

        self.rt_md_df = rt_md_df
        self.symbol_info = symbol_info
        self.signal_df_list = signal_df_list

    def cal_all_target_position(
        self,
        account: str,
        money: float,
        signal_df_list: list,
        rt_md_df: pd.DataFrame,
        symbol_info: pd.DataFrame,
    ):
        """
        计算多个账户的目标持仓
        :param account:账户名称
        :param money:要交易的资金量
        :param signal_df_list:
        :param rt_md_df:
        :param symbol_info:
        :return:
        """
        for signal_df in signal_df_list:
            if signal_df.empty:
                print(signal_df, "signal error")

        target_signal_s = pd.concat(signal_df_list).groupby("symbol")["value"].sum()
        target_position_s = self.cal_target_position(
            money, target_signal_s, rt_md_df, symbol_info
        )

        return {account: target_position_s}

    def cal_target_position_by_weight(
        self,
        money: float,
        signal: pd.Series,
        weight: pd.Series,
        rt_md_df: pd.DataFrame,
        symbol_info: pd.DataFrame,
    ):
        """
        加权计算目标仓位
        :param account:
        :param money:
        :param weight:
        :param rt_md_df:
        :param symbol_info:
        :return:
        """
        if weight is None:
            weight = pd.Series(1 / signal.shape[0], index=signal.index)

        rt_md_df = rt_md_df.reset_index().set_index("symbol")
        rt_md_df["exchange_ctp"] = [
            symbol_info["exchange_ctp"][x] for x in rt_md_df.index
        ]
        price = rt_md_df["close"]

        ss = ((money * weight * signal) / symbol_info["multiplier"] / price).dropna()
        target_position_s = ss.apply(lambda x: self.round_or_ceil(x))

        target_position_s.index = rt_md_df["contract"][ss.index]
        target_position_s.index = [
            self.get_trade_code(contract, symbol_info)
            for contract in target_position_s.index
        ]
        return target_position_s

    def cal_rt_target_position(self, account: str, money: float):
        """
        计算实时的目标仓位
        :param account:账户名称
        :param money:资金量大小
        :return:
        """
        target_position = self.cal_all_target_position(
            account=account,
            money=money,
            signal_df_list=self.signal_df_list,
            rt_md_df=self.rt_md_df,
            symbol_info=self.symbol_info,
        )
        return target_position
