from typing import Union

import pandas as pd
import pyarrow.parquet as pq


class CnFutureMd1d:
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        factor_define的基类,继承该类中的数据,产生因子
        :param md_data:期货日行情数据
        """
        if md_data is None:
            md_data = pq.read_table(
                "/mnt/gitee/quanthub/datahub/raw/cn/future/md/main_1d_o_m.parquet",
                filters=[
                    ("symbol", "not in", ["IH", "IC", "IF"]),
                    ("turnover", ">", 10 * 10000 * 10000),
                ],
            ).to_pandas()
            # md_data.set_index(["trading_date", 'symbol'], inplace=True)
        else:
            md_data = md_data

        if md_data.index.names != ["trading_date", "symbol"]:
            md_data.set_index(["trading_date", "symbol"], inplace=True)

        md_data["ret_1d"] = md_data["close"] / md_data["pre_close"] - 1

        self.ret_1d_df = md_data["ret_1d"].unstack()
        self.open_df = md_data["open"].unstack()
        self.close_df = md_data["close"].unstack()
        self.high_df = md_data["high"].unstack()
        self.low_df = md_data["low"].unstack()
        self.vol_df = md_data["volume"].unstack()
        self.pre_close_df = md_data["pre_close"].unstack()
        self.turnover_df = md_data["turnover"].unstack()


class CnFutureMd1m:
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        factor_define的基类,继承该类中的数据,产生因子
        :param md_data:期货分钟行情数据
        """
        pass


class CnFutureMasterData:
    def __init__(self):
        print("调用了 CnFutureMasterData")
        pass


class CnStockMd1d:
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        factor_define的基类,继承该类中的数据,产生因子
        :param md_data:股票日行情数据
        """
        if md_data is None:
            md_data = pq.read_table(
                "/mnt/gitee/quanthub/datahub/raw/cn/stock/md/hfq_1d.parquet",
            ).to_pandas()
        else:
            md_data = md_data

        if md_data.index.names != ["trading_date", "code"]:
            md_data.set_index(["trading_date", "code"], inplace=True)

        md_data["ret_1d"] = md_data["close"] / md_data["pre_close"] - 1

        self.ret_1d_df = md_data["ret_1d"].unstack()
        self.open_df = md_data["open"].unstack()
        self.close_df = md_data["close"].unstack()
        self.high_df = md_data["high"].unstack()
        self.low_df = md_data["low"].unstack()
        self.vol_df = md_data["volume"].unstack()
        self.pre_close_df = md_data["pre_close"].unstack()
        self.turnover_df = md_data["turnover"].unstack()


class CnStockMd1m:
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        factor_define的基类,继承该类中的数据,产生因子
        :param md_data:股票分钟行情数据
        """
        if md_data is None:
            md_data = pq.read_table(
                "/mnt/gitee/quanthub/datahub/raw/cn/stock/md/hfq_1m/",
            ).to_pandas()
        else:
            md_data = md_data

        if md_data.index.names != ["trading_date", "code"]:
            md_data.set_index(["trading_date", "code"], inplace=True)

        md_data["ret_1m"] = md_data["close"] / md_data["pre_close"] - 1

        self.ret_1m_df = md_data["ret_1m"].unstack()
        self.open_df = md_data["open"].unstack()
        self.close_df = md_data["close"].unstack()
        self.high_df = md_data["high"].unstack()
        self.low_df = md_data["low"].unstack()
        self.vol_df = md_data["volume"].unstack()
        self.pre_close_df = md_data["pre_close"].unstack()
        self.turnover_df = md_data["turnover"].unstack()


