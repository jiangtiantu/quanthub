from datetime import timedelta, date
from typing import Union

from plutus.data.data_base import DataBase
from plutus.utils.tool.logger import log_record

logger = log_record(__file__, "data")


class PretreatBase(DataBase):
    def __init__(self, data_dir: Union[str, None] = None, dt_delta: int = 0):
        """
        对数据进行预处理的基类,pretreat 对数据类型,字段名称做修改
        :param data_dir:存储路径
        :param dt_delta:间隔时间
        """
        super(PretreatBase, self).__init__()
        self.data_dir = data_dir
        self.dt_delta = dt_delta
        self.today = date.today()
        self.end_date = self.today.strftime("%Y-%m-%d")
        self.start_date = (date.today() - timedelta(self.dt_delta)).strftime("%Y-%m-%d")
