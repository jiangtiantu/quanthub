from datetime import date, datetime, timedelta
from typing import Union

from plutus.data.data_base import DataBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class PrepareBase(DataBase):
    def __init__(self, data_dir: str, dt_delta: int):
        """
        将数据库中的数据准备到实际生产环境和研究环境
        :param data_dir:数据储存地址
        :param dt_delta:间接dt_delta 个交易日
        """
        super(PrepareBase, self).__init__()

        self.today = date.today()
        self.data_dir = data_dir
        self.dt_delta = dt_delta
        self.end_date = self.today.strftime("%Y-%m-%d")
        self.start_date = (datetime.today() - timedelta(dt_delta)).strftime("%Y-%m-%d")

    def get_trading_date_info(
        self, start_date: Union[str, None] = None, end_date: Union[str, None] = None
    ):
        """
        从数据库中获取交易信息
        :return:
        """
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.end_date
        self.ck_control.read_df(
            db="commercial_cn_future_master",
            tb="trading_date_info",
            filters=[
                ("trading_date", ">=", f"'{start_date} 00:00:00.000'"),
                ("trading_date", "<=", f"'{end_date} 00:00:00.000'"),
            ],
        )


if __name__ == "__main__":
    prepare_base = PrepareBase()
