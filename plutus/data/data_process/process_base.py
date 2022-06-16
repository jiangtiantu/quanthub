from datetime import timedelta, date

from plutus.data.data_base import DataBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class ProcessBase(DataBase):
    def __init__(self, data_dir: str, dt_delta: int):
        """
        对预处理的数据,进一步加工,产生新数据
        :param data_dir:
        :param dt_delta:
        """
        super(ProcessBase, self).__init__()
        self.data_dir = data_dir
        self.dt_delta = dt_delta
        self.today = date.today()
        self.end_date = self.today.strftime("%Y-%m-%d")
        self.start_date = (date.today() - timedelta(self.dt_delta)).strftime("%Y-%m-%d")
