from typing import Union

import pandas as pd

from plutus.data.data_pretreat.pretreat_base import PretreatBase


class PretreatBS(PretreatBase):
    def __init__(
        self,
        data_dir: str = "/mnt/datadisk/data/",
        dt_delta: int = 5,
    ):
        """
        预处理从bs 获取的数据
        :param data_dir:
        :param dt_delta:
        """
        super(PretreatBS, self).__init__(data_dir=data_dir, dt_delta=dt_delta)

    def pretreat_cn_stock_master_trading_date_info(
        self, df: Union[pd.DataFrame, None] = None
    ):
        """
        预处理股票交易日数据
        :param df:
        :return:
        """
        if df is None:
            df = self.read_parquet(
                db="raw/cn/stock/master/", tb="trading_date_info_bs.parquet"
            )
        return df

    def pretreat_cn_stock_master_code_info(self, df: Union[pd.DataFrame, None] = None):
        """
        预处理股票基础信息数据
        :param df:
        :return:
        """
        df.rename(
            columns={
                "ipoDate": "listing_date",
                "outDate": "delisting_date",
            },
            inplace=True,
        )
        df["code"] = df["code"].str.split(".").str[1]

        return df

    def pretreat_cn_stock_md_all_1d(
        self,
        df: Union[pd.DataFrame, None] = None,
    ):
        """
        预处理股票日行情数据
        :param df:
        :return:
        """
        df.rename(
            columns={
                "preclose": "pre_close",
                "amount": "turnover",
                "pctChg": "pct_chg",
                "isST": "is_st",
            },
            inplace=True,
        )
        df["code"] = df["code"].str.split(".").str[1]

        pretreated_df = df[
            [
                "trading_date",
                "code",
                "turnover",
                "low",
                "high",
                "open",
                "volume",
                "close",
                "pre_close",
                "pct_chg",
                "is_st",
            ]
        ]
        return pretreated_df

    def pretreat_cn_stock_md_adjust_factor(
        self,
        df: Union[pd.DataFrame, None] = None,
    ):
        """
        股票的复权因子
        :param df:
        :return:
        """
        df.rename(
            columns={
                "dividOperateDate": "divid_operate_date",
                "foreAdjustFactor": "qfq_factor",
                "backAdjustFactor": "hfq_factor",
                "adjustFactor": "adjust_factor",
            },
            inplace=True,
        )
        df["code"] = df["code"].str.split(".").str[1]

        pretreated_df = df[
            [
                "code",
                "divid_operate_date",
                "qfq_factor",
                "hfq_factor",
            ]
        ]
        return pretreated_df

    def pretreat_cn_stock_index_constituent_info(
        self,
        df: Union[pd.DataFrame, None] = None,
    ):
        """
        股票指数的成分
        :param df:
        :return:
        """

        df["code"] = df["code"].str.split(".").str[1]

        pretreated_df = df
        return pretreated_df

    def pretreat_cn_stock_index_industry_sw1(
        self,
        df: Union[pd.DataFrame, None] = None,
    ):
        """
        股票指数的成分
        :param df:
        :return:
        """

        df["code"] = df["code"].str.split(".").str[1]

        pretreated_df = df
        return pretreated_df
