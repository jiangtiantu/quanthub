"""
This is a customized error library.
"""


class DatetimeError(Exception):
    def __init__(self, msg):
        """
        日期类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class DatabaseError(Exception):
    def __init__(self, msg):
        """
        数据库类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class FileError(Exception):
    def __init__(self, msg):
        """
        文件类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class JsonError(Exception):
    def __init__(self, msg):
        """
        json类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class LogError(Exception):
    def __init__(self, msg):
        """
        日志类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class MathError(Exception):
    def __init__(self, msg):
        """
        数学类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class NetworkError(Exception):
    def __init__(self, msg):
        """
        网络类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class PathError(Exception):
    def __init__(self, msg):
        """
        路径类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class ProcessError(Exception):
    def __init__(self, msg):
        """
        进程类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class RegexError(Exception):
    def __init__(self, msg):
        """
        正则类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class SqlError(Exception):
    def __init__(self, msg):
        """
        sql类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class StringError(Exception):
    def __init__(self, msg):
        """
        字符串类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class TimeError(Exception):
    def __init__(self, msg):
        """
        时间类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class UrlError(Exception):
    def __init__(self, msg):
        """
        url类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class XmlError(Exception):
    def __init__(self, msg):
        """
        xml类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class ZipError(Exception):
    def __init__(self, msg):
        """
        zip类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class ZlibError(Exception):
    def __init__(self, msg):
        """
        zlib类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg


class ExceptionError(Exception):
    def __init__(self, msg):
        """
        异常类错误
        :param msg:
        """
        super().__init__(msg)
        self.msg = msg
