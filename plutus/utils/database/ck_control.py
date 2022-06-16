import re
import time
import warnings
from typing import Union, List

import clickhouse_driver as ck_driver
import pandas as pd

from plutus.utils.exception.error import DatabaseError
from plutus.utils.tool.configer import Configer
from plutus.utils.tool.logger import log_record

warnings.filterwarnings("ignore")

logger = log_record(__file__, "database")


class ClickHouse:
    def __init__(
        self,
        host: Union[str, None] = None,
        port: Union[int, None] = None,
        user: Union[str, None] = None,
        pwd: Union[str, None] = None,
    ):
        """
        控制clickhouse,读写改删
        :param host:
        :param port:
        :param user:
        :param pwd:
        """
        conf_ = Configer()
        config = conf_.get_config
        host = config.get("clickhouse", "host") if host is None else host
        port = config.getint("clickhouse", "port") if port is None else port
        user = config.get("clickhouse", "user") if user is None else user
        password = config.get("clickhouse", "password") if pwd is None else pwd
        self.client = ck_driver.Client(
            host=host, port=port, user=user, password=password
        )

    def execute_sql(self, sql_str: str):
        """
        执行sql 语句
        :param sql_str:
        :return:
        """
        return self.client.execute(sql_str)

    def create_db(self, db: str, engine: str = "Atomic"):
        """
        创建数据库
        :param db:
        :param engine:
        :return:
        """
        create_database_sql = f"CREATE DATABASE IF NOT EXISTS {db} engine={engine}"
        self.client.execute(create_database_sql)

    def create_tb(
        self,
        df: pd.DataFrame,
        db: str,
        tb: str,
        ind: list,
        partition: Union[list, None] = None,
    ):
        """
        Automated table builder. Hell yeah!
        :param df:dataframe
        :param db:数据库名称
        :param tb:表名
        :param ind:索引,按照ind 进项排序
        :param partition:按照partition进行分区
        :return:
        """
        if isinstance(ind, list) is False or len(ind) == 0:
            raise DatabaseError(
                "Index Declaration is a MUST-DO if you want to use clickhouse as your database."
            )
        datatype_dic = self.__map_table_types(df)
        cont_ = ",".join(
            [
                f"`{k}` {v}" if k not in ind else f"`{k}` {v} NOT NULL"
                for k, v in datatype_dic.items()
            ]
        )
        sql_ = (
            f"CREATE TABLE IF NOT EXISTS {db}.{tb} "
            f"({cont_}) "
            f"ENGINE = ReplacingMergeTree() "
        )
        appendix_ = (
            f"ORDER BY ({','.join(ind)})  "
            if ind is not None and len(ind) != 0
            else ","
        )
        appendix_ += (
            f"PARTITION BY ({','.join(partition)}) "
            if partition is not None and len(partition) != 0
            else ""
        )
        sql_ += appendix_
        self.execute_sql(sql_)

    def __map_table_types(self, df: pd.DataFrame):
        """
        to map dataframe type into clickhouse table type.
        :param df:
        :return:
        """
        type_dic = df.dtypes.to_dict()
        type_dic_for_ck = {}
        for k, v in type_dic.items():
            if "int" in str(v).lower() or "float" in str(v).lower():
                type_dic_for_ck[k] = "Float64"
            elif "date" in str(v).lower() or "time" in str(v).lower():
                type_dic_for_ck[k] = "Datetime64"
            else:
                type_dic_for_ck[k] = "String"
        return type_dic_for_ck

    def __trans_df_types(self, df: pd.DataFrame):
        """
        转换dataframe 的数据类型为clickhouse数据类型
        :param df:
        :return:
        """
        type_dic = df.dtypes.to_dict()
        for k, v in type_dic.items():
            if "int" in str(v).lower() or "float" in str(v).lower():
                df[k] = df[k].astype("float")
            elif "date" in str(v).lower() or "time" in str(v).lower():
                df[k] = pd.to_datetime(df[k])
            else:
                df[k] = df[k].astype("str").fillna(",")
        return df

    def get_table_type_dic(self, table):
        pass

    def read_df_by_sql_str(self, sql_str):
        """
        通过sql语句读取dataframe,不做排序整理
        :param sql_str:
        :return:
        """
        data, columns = self.client.execute(
            sql_str, columnar=True, with_column_types=True
        )
        if data:
            df = pd.DataFrame(
                {
                    re.sub(r"\W", "_", col[0]): pd.to_datetime(d)
                    if "date" in col[1].lower() or "time" in col[1].lower()
                    else d
                    for d, col in zip(data, columns)
                }
            )
            return df
        else:
            df = pd.DataFrame({}, columns=[col[0] for col in columns])
            return df

    def has_tb(
        self,
        df: pd.DataFrame,
        db: str,
        tb: str,
        ind: Union[list, None] = None,
        partition: Union[list, None] = None,
    ):
        """
        check if target database or table exits, build if not.
        :param df:
        :param db:
        :param tb:
        :param ind:
        :param partition:
        :return:
        """

        has_tb_ = self.execute_sql(f"exists {db}.{tb}")
        if has_tb_[0][0]:
            return
        else:
            has_db_ = self.execute_sql(f"exists {db}")
            if not has_db_[0][0]:
                self.create_db(db)
            self.create_tb(df, db, tb, ind, partition=partition)
            time.sleep(0.5)

    def to_sql(self, df, db, table):
        """
        将dataframe存到clickhouse中,需要自己提前建表
        :param df:
        :param db:
        :param table:
        :return:
        """
        cols = ",".join(df.columns.tolist())
        df = self.__trans_df_types(df)
        data = df.to_dict("records")
        sql_ = f"INSERT INTO {db}.{table} ({cols}) VALUES"
        self.client.execute(sql_, data, types_check=True)

    def get_db(self):
        """
        获取数据库的名字
        :return:
        """
        sql_str = "SHOW DATABASES"
        dbs = self.client.execute(sql_str)
        return dbs

    def get_tb(self):
        """
        获取clickhouse 表名
        :return:
        """
        pass

    def get_col_name(self, db: str):
        """
        获取clickhouse 表名
        :param db:
        :return:
        """
        sql_str = f"SELECT name FROM system.tables WHERE database = '{db}';"
        col_ls = self.client.execute(sql_str)
        col_ls = [i[0] for i in col_ls] if len(col_ls) != 0 else []
        return col_ls

    def insert_df(
        self,
        df: pd.DataFrame,
        db: str,
        tb: str,
        ind: Union[list, None] = None,
        partition: Union[list, None] = None,
    ):
        """
        将dataframe插入到clickhouse中,不需要自己自动建表
        :param df:
        :param db:
        :param tb:
        :param ind:
        :param partition:
        :return:
        """
        self.has_tb(df, db, tb, ind, partition)

        if partition is not None and len(partition) != 0:
            for _, v in df.groupby(partition):
                self.to_sql(v, db, tb)
        else:
            self.to_sql(df, db, tb)
        logger.info(f"Data inserted into {db}.{tb}: Dataframe{df.shape}")

    def read_df(self, db: str, tb: str, filters: Union[List[tuple], None] = None):
        """
        从clickhouse中读取dataframe

        :param db:
        :param tb:
        :param filters:
        :return:
        """
        if not filters:
            sql_str = f"select * from {db}.{tb}"
        else:
            sql_str_list = [" ".join((key, op, val)) for (key, op, val) in filters]
            sql_str = f"select * from {db}.{tb} where {' and '.join(sql_str_list)} "
            print(sql_str)

        df = self.read_df_by_sql_str(sql_str)
        return df

    def drop_db(self, db: str):
        """
        删除clickhouse 中某个数据库
        :param db:
        :return:
        """
        drop_sql = f"DROP DATABASE IF EXISTS {db}"
        self.client.execute(drop_sql)

    def drop_tb(self, db: str, tb: str):
        """
        删除clickhouse 中某个数据表
        :param db:
        :param tb:
        :return:
        """
        drop_sql = f"DROP TABLE IF EXISTS {db}.{tb}"
        self.client.execute(drop_sql)

    def drop_duplicate_data(self, db: str, tb: str):
        """
        对clickhouse 中的数据去重
        :param db:
        :param tb:
        :return:
        """
        drop_duplicate_data_sql = f" OPTIMIZE TABLE {db}.{tb} final"
        self.client.execute(drop_duplicate_data_sql)
