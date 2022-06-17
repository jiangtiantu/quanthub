import configparser
import os


class Configer:
    def __init__(self):
        _fp = os.path.dirname(__file__)
        self.root_dir = os.path.realpath(
            os.path.join(_fp, os.sep.join(["..", "..", ".."]))
        )
        self.config_path = os.path.join(self.root_dir, "plutus/config/")

    @property
    def get_config(self):
        """
        获取配置信息
        :return:
        """
        _conf_path = os.path.join(self.config_path, "config.ini")

        config = configparser.ConfigParser()
        config.read(_conf_path)
        return config


if __name__ == "__main__":
    Configer()
