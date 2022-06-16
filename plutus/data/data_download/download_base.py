from datetime import timedelta, date

from plutus.data.data_base import DataBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class DownloadBase(DataBase):
    def __init__(self, data_dir: str, dt_delta: int):
        """
        download 的基类
        :param data_dir: 数据存放路径
        :param dt_delta: 时间间隔
        """
        super(DownloadBase, self).__init__()
        self.data_dir = data_dir
        self.dt_delta = dt_delta
        self.today = date.today()
        self.end_date = self.today.strftime("%Y-%m-%d")
        self.start_date = (date.today() - timedelta(self.dt_delta)).strftime("%Y-%m-%d")
