from plutus.utils.database.database_control import DatabaseControl


class SignalBase(DatabaseControl):
    def __init__(self, signalhub_dir: str):
        """
        计算交易信号的基类
        :param signalhub_dir:交易信号的存放路径
        """
        super(SignalBase, self).__init__()
        self.signalhub_dir = signalhub_dir
