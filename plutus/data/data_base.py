from plutus.utils.database.database_control import DatabaseControl


class DataBase(DatabaseControl):
    def __init__(self):
        """
        data 模块的基类
        :param data_dir:数据储存路径
        """
        super(DataBase, self).__init__()
