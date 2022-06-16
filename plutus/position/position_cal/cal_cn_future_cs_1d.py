from typing import Union

import pandas as pd

from plutus.position.position_cal.cal_position_base import (
    CalPosition,
)


class CalPositionMom(CalPosition):
    def __init__(
        self,
        position_dir: str = "/mnt/gitee/quanthub/position/",
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
