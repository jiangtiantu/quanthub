import pandas as pd

from plutus.factor.factor_base import FactorBase


class CalFactor(FactorBase):
    def __init__(self, factorhub_dir: str):
        """
        计算因子的基类
        :param factorhub_dir:因子存放路径
        """
        super(CalFactor, self).__init__(factorhub_dir)

    def cal_all_factor(self, factor_obj):
        """
        计算全部因子
        :param factor_obj:因子类实例
        :return:
        """
        factor_df_list = []
        factor_name_list = [fac for fac in dir(factor_obj) if fac[0:7] == "factor_"]
        for factor_name in factor_name_list:
            factor_df = self.cal_factor(factor_obj, factor_name)
            factor_df_list.append(factor_df)
        return factor_df_list

    @staticmethod
    def cal_factor(factor_obj: object, factor_name: str):
        """
        计算单个因子
        :param factor_obj:因子实例
        :param factor_name:因子名
        :return:
        """
        factor_df = getattr(factor_obj, factor_name)()
        factor_df = pd.DataFrame(factor_df.stack(), columns=["value"]).reset_index()
        factor_df["name"] = factor_name
        factor_df["type"] = factor_obj.__class__.__name__
        return factor_df

    def cal_and_save_all_factor(self, factor_obj, db: str, tb: str):
        pass


class CalCS(CalFactor):
    def __init__(self, factorhub_dir: str):
        """
        计算因子的基类
        :param factorhub_dir:因子存放路径
        """
        super(CalCS, self).__init__(factorhub_dir)


class CalTS(CalFactor):
    def __init__(self, factorhub_dir: str):
        """
        计算因子的基类
        :param factorhub_dir:因子存放路径
        """
        super(CalTS, self).__init__(factorhub_dir)
