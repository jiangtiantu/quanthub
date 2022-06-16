import os
from typing import Union, List

import pandas as pd
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

from plutus.utils.database.ck_control import ClickHouse
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class DatabaseControl:
    def __init__(self):
        """
        data 模块的基类
        :param data_dir:数据储存路径
        """
        self.ck_control = ClickHouse()

    def has_file_dir(self, file_dir: str):
        """
        检查是否存在文件路径,不存在创建之
        :param file_dir:文件路径
        """
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    def save_parquet(
        self,
        df: pd.DataFrame,
        data_dir: str = "",
        db: str = None,
        tb: str = None,
    ):
        """
        将dataframe 存为parquet文件
        :param data_dir:
        :param df:dataframe
        :param db:db
        :param tb:table
        :return:
        """

        if ".parquet" not in tb:
            tb_dir = f"{data_dir}{db}{tb}"
            self.has_file_dir(tb_dir)
            if "trading_date" in df.columns and len(df.columns) > 1:
                for (trading_dt, temp_df) in df.groupby(["trading_date"]):
                    if not temp_df.empty:
                        temp_df.to_parquet(f"{tb_dir}{str(trading_dt)[:10]}.parquet")
                    else:
                        print(f"{trading_dt} is None")
        else:
            tb_dir = f"{data_dir}{db}{tb}"
            self.has_file_dir(f"{data_dir}{db}")
            table_ = pa.Table.from_pandas(df)
            pq.write_table(table_, tb_dir)

        logger.info(f"Data inserted into parquet {db}.{tb}: Dataframe{df.shape}")

    def read_parquet(
        self,
        data_dir: str = "",
        db: str = "",
        tb: str = "",
        filters: Union[List[tuple], None] = None,
    ):
        """
        读取parquet文件为dataframe
        :param data_dir:
        :param db:
        :param tb:
        :param filters:
        :return:
        """

        tb_dir = f"{data_dir}{db}{tb}"
        df = pq.read_table(tb_dir, filters=filters).to_pandas()
        return df

    def save_clickhouse(
        self,
        df: pd.DataFrame,
        db: str,
        tb: str,
        ind: Union[list, None] = None,
        partition: Union[list, None] = None,
    ):
        """
        将数据存到clickhouse
        :param df:dataframe
        :param db:数据库名字
        :param tb:表名
        :param ind:按ind 索引排序
        :param partition:按partition 分区
        :return:
        """
        self.ck_control.insert_df(df, db, tb, ind, partition)
        logger.info(f"Data inserted into clickhouse {db}.{tb}: Dataframe{df.shape}")

    def read_clickhouse(
        self, db: str, tb: str, filters: Union[List[tuple], None] = None
    ):
        """
        从clickhouse 中读取数据
        :param db:数据库名
        :param tb:表明
        :param filters:筛选条件
        :return:
        """
        df = self.ck_control.read_df(db, tb, filters)
        return df

    def save_csv(
        self, df: pd.DataFrame, data_dir: str = "", db: str = "", tb: str = ""
    ):
        """
        将数据存到csv
        :param data_dir:
        :param df:
        :param db:
        :param tb:
        :return:
        """
        tb_dir = f"{data_dir}{db}{tb}"
        table = pa.table(df)
        pc.write_csv(table, tb_dir)
        logger.info(f"Data inserted into csv {db}.{tb}: Dataframe{df.shape}")

    def read_csv(
        self, data_dir: str, db: str, tb: str, filters: Union[List[tuple], None] = None
    ):
        """
        从csv中读取数据
        :param data_dir:
        :param db:
        :param tb:
        :param filters:
        :return:
        """
        tb_dir = f"{data_dir}{db}{tb}"
        df = pc.read_csv(tb_dir, filters).to_pandas()
        return df
