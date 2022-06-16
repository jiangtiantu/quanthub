from typing import Union

import pandas as pd

from plutus.data.data_prepare.prepare_center_data import CnFutureMd1d


class Mom(CnFutureMd1d):
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """

        :param md_data:
        """
        super(Mom, self).__init__(md_data)

    def factor_ts_1d_example1(self, close: Union[pd.DataFrame, None] = None):
        """

        :param close:
        :return:
        """
        if close is None:
            close = self.close_df
        factor = -1 * close.pct_change(5)
        return factor

    def factor_ts_1d_example2(self, close: Union[pd.DataFrame, None] = None):
        """

        :param close:
        :return:
        """
        if close is None:
            close = self.close_df
        factor = -1 * close.pct_change(10)
        return factor
