from plutus.utils.database.database_control import DatabaseControl


class FactorBase(DatabaseControl):
    def __init__(self, factorhub_dir: str):
        """
        因子计算的基类
        :param factorhub_dir:因子存放路径
        """
        super(FactorBase, self).__init__()
        self.factorhub_dir = factorhub_dir
