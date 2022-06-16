from datetime import datetime
from typing import Any


def map_datetime(dt_string: Any):
    """

    :param dt_string:
    :return:
    """
    if not isinstance(dt_string, str):
        return None
    elif len(dt_string) == 10:
        return datetime.strptime(dt_string, "%Y-%m-%d")
    elif len(dt_string) == 19:
        return datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    elif len(dt_string) > 19:
        dates = dt_string.split(" ")[0]
        times = dt_string.split(" ")[1].split(".")[0]
        mils = dt_string.split(" ")[1].split(".")[1].rstrip("0")
        mils = mils.ljust(3, "0")
        return datetime(
            year=int(dates.split("-")[0]),
            month=int(dates.split("-")[1]),
            day=int(dates.split("-")[2]),
            hour=int(times.split(":")[0]),
            minute=int(times.split(":")[1]),
            second=int(times.split(":")[2]),
            microsecond=int(mils) * 1000,
        )
