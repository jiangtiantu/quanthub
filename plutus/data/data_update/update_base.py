from datetime import date, datetime, timedelta

from plutus.data.data_base import DataBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class UpdateBase(DataBase):
    def __init__(self, data_dir: str, dt_delta: int):
        """
        更新raw、pretreat、process,commercial数据 的基类
        :param data_dir:
        :param dt_delta:
        """
        super(UpdateBase, self).__init__()
        self.data_dir = data_dir
        self.dt_delta = dt_delta

        self.today = date.today()
        self.end_date = self.today.strftime("%Y-%m-%d")
        self.start_date = (datetime.today() - timedelta(dt_delta)).strftime("%Y-%m-%d")
        self.trading_date_info_s = self.get_trading_date_info()["trading_date"]

    def get_trading_date_info(self):
        df = self.ck_control.read_df(
            db="commercial_cn_future_master", tb="trading_date_info"
        )
        return df
