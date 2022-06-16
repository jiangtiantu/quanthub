from typing import Union

import baostock as bs
import pandas as pd

from plutus.data.data_download.download_base import DownloadBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class DownloadBS(DownloadBase):
    def __init__(self, data_dir: str = "/mnt/datadisk/data/", dt_delta: int = 5):
        """
        从baostock下载数据
        :param data_dir: 数据存放路径
        :param dt_delta: 时间间隔
        """
        super(DownloadBS, self).__init__(data_dir, dt_delta)

        login_bs = bs.login()
        logger.info("login respond error_code:" + login_bs.error_code)
        logger.info("login respond  error_msg:" + login_bs.error_msg)

        self.bs = bs

        self.trading_date_info = self.download_cn_stock_master_trading_date_info(
            end_date=self.end_date
        )

    def download_cn_stock_master_trading_date_info(
        self, start_date: str = "2010-01-01", end_date: str = "2023-01-01"
    ):
        """
        获取股票交易日信息
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: trading_date_info,一个dataframe
        """

        rs = self.bs.query_trade_dates(start_date=start_date, end_date=end_date)
        if rs.error_code == "0":
            df = rs.get_data()
            trading_date_info = df.loc[df["is_trading_day"] == "1"][["calendar_date"]]
            trading_date_info.rename(
                {"calendar_date": "trading_date"}, inplace=True, axis=1
            )
            trading_date_info["trading_date"] = pd.to_datetime(
                trading_date_info["trading_date"]
            )
            return trading_date_info
        else:
            logger.info(
                f"download_cn_trading_date_info is error ,{rs.error_code} ,{rs.error_msg} "
            )

    def download_cn_stock_master_code_info(self, given_date: Union[str, None] = None):

        k_rs = self.bs.query_stock_basic()
        data_df = k_rs.get_data()
        return data_df

    def download_cn_stock_md_all_1d(
        self,
        code_list: Union[list, None] = None,
        start_date: Union[str, None] = None,
        end_date: Union[str, None] = None,
    ):

        if code_list is None:
            code_list = self.bs.query_all_stock(end_date).get_data()["code"].tolist()

        data_df_list = []
        for code in code_list:
            print(code)
            k_rs = self.bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                start_date,
                end_date,
            )
            df = k_rs.get_data()
            if not df.empty:
                data_df_list.append(df)

        all_data_df = pd.concat(data_df_list)
        all_data_df.rename({"date": "trading_date"}, inplace=True, axis=1)
        all_data_df["trading_date"] = pd.to_datetime(all_data_df["trading_date"])

        return all_data_df

    def download_cn_stock_md_adjust_factor(
        self,
        code_list: Union[list, None] = None,
        start_date: Union[str, None] = None,
        end_date: Union[str, None] = None,
    ):

        if code_list is None:
            code_list = self.bs.query_all_stock(end_date).get_data()["code"].tolist()

        data_df_list = []
        for code in code_list:
            k_rs = self.bs.query_adjust_factor(
                code,
                start_date,
                end_date,
            )
            df = k_rs.get_data()
            if not df.empty:
                data_df_list.append(df)
        all_data_df = pd.concat(data_df_list)
        return all_data_df

    def download_cn_stock_index_constituent_info(self, given_date: str):
        """
        获取指数成分股
        :param given_date: 交易日
        :return: 指数成分,一个dataframe
        """
        hs300_stock = self.bs.query_hs300_stocks(given_date).get_data()
        hs300_stock["index_code"] = "000300"
        zz500_stock = self.bs.query_zz500_stocks(given_date).get_data()
        zz500_stock["index_code"] = "000905"
        sz50_stock = self.bs.query_sz50_stocks(given_date).get_data()
        sz50_stock["index_code"] = "000016"

        all_stock = pd.concat([hs300_stock, zz500_stock, sz50_stock], axis=0)
        all_stock.rename({"updateDate": "trading_date"}, inplace=True, axis=1)
        all_stock["trading_date"] = pd.to_datetime(all_stock["trading_date"])

        return all_stock

    def download_cn_stock_index_industry_sw1(self, given_date: str):
        """
        获取申万行业分类
        :param given_date:
        :return:
        """
        if given_date is None:
            given_date = self.end_date

        data_df = download_bs.bs.query_stock_industry(date=given_date).get_data()
        data_df["trading_date"] = pd.to_datetime(given_date)
        return data_df


if __name__ == "__main__":
    download_bs = DownloadBS()
    trading_date_info = download_bs.trading_date_info
    trading_date_info = download_bs.download_cn_stock_master_trading_date_info(
        start_date="2021-05-19"
    )
    trading_date_info = [i for i in trading_date_info if i < download_bs.end_date]
    code_list = download_bs.bs.query_all_stock().get_data()["code"].tolist()

    for trading_dt in trading_date_info["trading_date"]:
        print(trading_dt.strftime("%Y-%m-%d"))

        cn_stock_master_code_info = download_bs.download_cn_stock_master_code_info(
            trading_dt.strftime("%Y-%m-%d")
        )
        download_bs.save_parquet(
            cn_stock_master_code_info,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/master/",
            tb=f"code_info_bs.parquet",
        )

        cn_stock_md_all_1d = download_bs.download_cn_stock_md_all_1d(
            code_list, trading_dt.strftime("%Y-%m-%d"), trading_dt.strftime("%Y-%m-%d")
        )
        download_bs.save_parquet(
            cn_stock_master_code_info,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/md/",
            tb=f"all_1d/bs/{trading_dt.strftime('%Y-%m-%d')}.parquet",
        )

        cn_stock_md_adjust_factor = download_bs.download_cn_stock_md_adjust_factor(
            code_list, trading_dt.strftime("%Y-%m-%d"), trading_dt.strftime("%Y-%m-%d")
        )
        download_bs.save_parquet(
            cn_stock_md_adjust_factor,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/md/",
            tb=f"adjust_factor/bs/{trading_dt.strftime('%Y-%m-%d')}.parquet",
        )

        cn_stock_master_code_info = (
            download_bs.download_cn_stock_master_trading_date_info(
                trading_dt.strftime("%Y-%m-%d")
            )
        )
        download_bs.save_parquet(
            cn_stock_master_code_info,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/master/",
            tb=f"trading_date_info_bs.parquet",
        )

        cn_stock_index_constituent_info = (
            download_bs.download_cn_stock_index_constituent_info(
                trading_dt.strftime("%Y-%m-%d")
            )
        )
        download_bs.save_parquet(
            cn_stock_index_constituent_info,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/index/",
            tb=f"index_constituent_info/bs/{trading_dt.strftime('%Y-%m-%d')}.parquet",
        )

        cn_stock_index_industry_sw1 = download_bs.download_cn_stock_index_industry_sw1(
            given_date=trading_dt.strftime("%Y-%m-%d")
        )
        download_bs.save_parquet(
            cn_stock_index_industry_sw1,
            data_dir="/mnt/datadisk/data/",
            db="raw/cn/stock/index/",
            tb=f"industry_sw1/bs/{trading_dt.strftime('%Y-%m-%d')}.parquet",
        )
