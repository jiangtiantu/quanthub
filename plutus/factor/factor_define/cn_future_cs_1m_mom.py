from typing import Union

import pandas as pd

from plutus.data.data_prepare.prepare_center_data import CnFutureMd1m


class Mom(CnFutureMd1m):
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        因子定义文件
        :param md_data:日行情数据
        """
        super(Mom, self).__init__(md_data)

    def factor_cs_1d_example1(self):
        """
        示例因子1
        :param close:
        :return:
        """
        pass

    def factor_cs_1d_example2(self):
        """
        示例因子2
        :param close:
        :return:
        """
        pass
