from string import digits

import pandas as pd

from plutus.position.position_base import PositionBase


class CalPosition(PositionBase):
    def __init__(self, position_dir: str):
        """
        计算仓位的基类
        :param position_dir:持仓文件存路径
        """
        super(CalPosition, self).__init__(position_dir)

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

    def cal_target_position(
        self,
        money: float,
        signal: pd.DataFrame,
        rt_md_df: pd.DataFrame,
        symbol_info: pd.DataFrame,
    ):
        """
        计算单个账户目标持仓
        :param money:资金量
        :param signal:交易信号
        :param rt_md_df:实时行情
        :param symbol_info:交易品种信息
        :return:
        """
        rt_md_df = rt_md_df.reset_index().set_index("symbol")
        rt_md_df["exchange_ctp"] = [
            symbol_info["exchange_ctp"][x] for x in rt_md_df.index
        ]
        price = rt_md_df["close"]

        ss = (
            (money * 100 / sum(abs(signal)))
            * signal
            / symbol_info["multiplier"]
            / price
            / 100
        ).dropna()
        ss = ss.apply(lambda x: self.round_or_ceil(x))
        target_position_s = ss.copy()

        target_position_s.index = rt_md_df["contract"][ss.index]
        target_position_s.index = [
            self.get_trade_code(contract, symbol_info)
            for contract in target_position_s.index
        ]
        return target_position_s

    def cal_target_position_by_weight(
        self,
        account: str,
        money: float,
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
        rt_md_df = rt_md_df.reset_index().set_index("symbol")
        rt_md_df["exchange_ctp"] = [
            symbol_info["exchange_ctp"][x] for x in rt_md_df.index
        ]
        price = rt_md_df["close"]

        ss = ((money * weight) / symbol_info["multiplier"] / price).dropna()
        ss = ss.apply(lambda x: self.round_or_ceil(x))
        target_position_s = ss.copy()

        target_position_s.index = rt_md_df["contract"][ss.index]
        target_position_s.index = [
            self.get_trade_code(contract, symbol_info)
            for contract in target_position_s.index
        ]
        return {account: target_position_s}

    @staticmethod
    def round_or_ceil(value: float):
        """
        将交易仓位四舍五入,最小1手
        :param value:
        :return:
        """
        if 1 > value > 0:
            return 1
        elif 0 > value > -1:
            return -1
        else:
            if value in [float("-inf"), float("inf")]:
                print(f"{value} is inf or -inf")
                return float("nan")
            else:
                return round(value)

    @staticmethod
    def get_trade_code(contract: str, symbol_info: pd.DataFrame):
        """
        获取交易代码
        :param contract:合约名称
        :param symbol_info:交易瓶中信息
        :return:
        """
        symbol = contract.translate(str.maketrans(",", ",", digits))
        if symbol_info.at[symbol, "exchange_ctp"] == "SHFE":
            return contract.lower()
        if symbol_info.at[symbol, "exchange_ctp"] == "INE":
            return contract.lower()
        if symbol_info.at[symbol, "exchange_ctp"] == "DCE":
            return contract.lower()
        if symbol_info.at[symbol, "exchange_ctp"] == "CFFEX":
            return contract.upper()
        if symbol_info.at[symbol, "exchange_ctp"] == "CZCE":
            return symbol.upper() + contract[-3:]
