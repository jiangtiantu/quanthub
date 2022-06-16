from plutus.utils.database.database_control import DatabaseControl


class PositionBase(DatabaseControl):
    def __init__(self, position_dir: str):
        """
        仓位计算基类
        :param position_dir:
        """
        super(PositionBase, self).__init__(position_dir)
        self.position_dir = position_dir
