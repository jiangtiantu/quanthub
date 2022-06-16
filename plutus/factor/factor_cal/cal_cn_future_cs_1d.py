from typing import Union

import pandas as pd

from plutus.factor.factor_cal.cal_factor_base import (
    CalFactor,
)
from plutus.factor.factor_define.cn_future_ts_1d_mom import Mom


class CalMom(CalFactor):
    def __init__(
        self,
        factorhub_dir: str = "/mnt/gitee/quanthub/factorhub/",
        md_data: Union[pd.DataFrame, None] = None,
    ):
        """
        批量计算动量因子
        :param factorhub_dir:因子存放路径
        :param md_data:日行情数据
        """
        super(CalMom, self).__init__(factorhub_dir)
        self.db = "raw/cn/future/cs/1d/"
        self.tb = "mom/"
        self.md_data = md_data
        self.factor_obj = Mom(self.md_data)

    def cal_all_mom_factor(self):
        """
        计算因子类文件中,全部的因子
        :return:
        """
        factor_df_list = self.cal_all_factor(self.factor_obj)
        return factor_df_list

    def cal_and_save_all_factor(
        self,
        factor_obj: Union[object, None] = None,
        db: Union[str, None] = None,
        tb: Union[str, None] = None,
    ):
        """

        :param factor_obj:
        :param db:
        :param tb:
        :return:
        """
        if factor_obj is None:
            factor_obj = self.factor_obj
        if db is None:
            db = self.db
        if tb is None:
            tb = self.tb

        factor_name_list = [fac for fac in dir(factor_obj) if fac[0:7] == "factor_"]
        for factor_name in factor_name_list:
            factor_df = self.cal_factor(factor_obj, factor_name)
            self.save_parquet(factor_df, db, f"{tb}{factor_name}/")


if __name__ == "__main__":
    cal_factor_mom = CalMom()
    cal_factor_mom.cal_and_save_all_factor()
    print("calculate his mom factor data")
