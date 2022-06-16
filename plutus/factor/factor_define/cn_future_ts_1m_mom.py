from typing import Union

import pandas as pd

from plutus.data.data_prepare.prepare_center_data import CnFutureMd1m


class Mom(CnFutureMd1m):
    def __init__(self, md_data: Union[pd.DataFrame, None] = None):
        """

        :param md_data:
        """
        super(Mom, self).__init__(md_data)

    def factor_ts_1m_example1(self, close: Union[pd.DataFrame, None] = None):
        pass
