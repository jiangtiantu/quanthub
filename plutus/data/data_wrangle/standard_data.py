import numpy as np


# 去极值
def n_mad(arr, n: int = 3):
    """
    绝对值差中位数法
    :param arr:
    :param n:
    :return:
    """
    median = np.median(arr)
    diff_median = np.median(np.abs(arr - median))
    max_range = median + n * diff_median
    min_range = median - n * diff_median
    return np.clip(arr, min_range, max_range)


def n_sigma(arr, n: int = 3):
    """
    标准差法
    :param arr:
    :param n:
    :return:
    """
    mean = np.mean(arr)
    std = np.std(arr)
    max_bond = mean + n * std
    min_bond = mean - n * std
    return np.clip(arr, min_bond, max_bond)


def percentile(arr, min_=0.025, max_=0.975):
    """
    百分位法
    :param arr:
    :param min_:
    :param max_:
    :return:
    """
    arr = np.sort(arr)
    q = np.quantile(arr, [min_, max_])
    return np.clip(arr, q[0], q[1])


# 标准化
def standard_z_score(arr: np.array):
    """
    Z-Score 标准化
    :param arr:
    :return:
    """
    std = np.std(arr)
    mean = np.mean(arr)
    return (arr - mean) / std


def standard_max_min(arr: np.array):
    """
    最大最小标准化
    :param arr:
    :return:
    """
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


# 缺失值填充
def fillna():
    pass
