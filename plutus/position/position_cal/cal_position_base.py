from plutus.position.position_base import PositionBase


class CalPosition(PositionBase):
    def __init__(self, position_dir: str):
        """
        计算仓位的基类
        :param position_dir:持仓文件存路径
        """
        super(CalPosition, self).__init__(position_dir)

    @staticmethod
    def round_or_ceil(value: float):
        """
        将交易仓位四舍五入,最小1手
        :param value:
        :return:
        """
        if 1 > value > 0:
            return 1
        elif 0 > value > -1:
            return -1
        else:
            if value in [float("-inf"), float("inf")]:
                print(f"{value} is inf or -inf")
                return float("nan")
            else:
                return round(value)
