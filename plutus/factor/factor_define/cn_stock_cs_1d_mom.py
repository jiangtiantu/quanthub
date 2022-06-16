from typing import Union

import pandas as pd

from plutus.data.data_prepare.prepare_center_data import CnStockMd1d


class Mom(CnStockMd1d):
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """
        因子定义文件
        :param md_data:日行情数据
        """
        super(Mom, self).__init__(md_data)

    def factor_cs_1d_example1(self, close: Union[pd.DataFrame, None] = None):
        """
        示例因子1
        :param close:
        :return:
        """
        if close is None:
            close = self.close_df
        factor = -1 * close.pct_change(5)
        return factor

    def factor_cs_1d_example2(self, close: Union[pd.DataFrame, None] = None):
        """
        示例因子2
        :param close:
        :return:
        """
        if close is None:
            close = self.close_df
        factor = -1 * close.pct_change(10)
        return factor
