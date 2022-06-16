import bottleneck as bn
import numpy as np
from numba import jit
from scipy.stats import kurtosis, skew


@jit(nopython=False)
def e_sign(arr: np.array):
    return np.sign(arr)


@jit(nopython=False)
def e_log(arr: np.array):
    return np.log(arr)


@jit(nopython=False)
def e_abs(arr: np.array):
    return np.abs(arr)


@jit(nopython=False)
def e_sqrt(arr: np.array):
    return np.sqrt(arr)


@jit(nopython=False)
def e_round(arr: np.array):
    return np.round(arr)


@jit(nopython=False)
def e_reciprocal(arr: np.array):
    return np.reciprocal(arr)


@jit(nopython=False)
def ts_shift(arr, window: int):
    e = np.empty_like(arr)
    if window >= 0:
        e[:window] = np.nan
        e[window:] = arr[:-window]
    else:
        e[window:] = np.nan
        e[:window] = arr[-window:]
    return e


@jit(nopython=False)
def ts_diff(arr: np.array, window: int):
    return arr - ts_shift(arr, window)


@jit(nopython=False)
def ts_pct(arr: np.array, window: int):
    return arr.pct_change(window)


@jit(nopython=False)
def ts_sum(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_sum(arr, window)


@jit(nopython=False)
def ts_mean(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_mean(arr, window)


@jit(nopython=False)
def ts_mad(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return np.abs(arr - bn.move_mean(arr, window)) / window


@jit(nopython=False)
def ts_std(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_std(arr, window)


@jit(nopython=False)
def ts_ptp(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_max(arr, window) - bn.move_min(arr, window)


@jit(nopython=False)
def ts_max(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_max(arr, window)


@jit(nopython=False)
def ts_min(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_min(arr, window)


@jit(nopython=False)
def ts_median(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_median(arr, window)


@jit(nopython=False)
def ts_rank(arr: np.array, window: int):
    arr = np.nan_to_num(arr)
    return bn.move_rank(arr, window)


@jit(nopython=False)
def ts_skewness(arr: np.array, window: int):
    y = np.full(len(arr), np.nan)
    for i in range(len(arr)):
        if i + 1 >= window:
            y[i] = skew(arr[i + 1 - window : i + 1], bias=False)
    return y


@jit(nopython=False)
def ts_kuriosis(arr: np.array, window: int):
    y = np.full(len(arr), np.nan)
    for i in range(len(arr)):
        if i + 1 >= window:
            y[i] = kurtosis(arr[i + 1 - window : i + 1], bias=False)
    return y


# def ts_quantile(arr,window: int):
#     return arr.rolling(window).median()


@jit(nopython=False)
def b_add(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.add(arr1, arr2)


@jit(nopython=False)
def b_sub(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.subtract(arr1, arr2)


@jit(nopython=False)
def b_mul(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.multiply(arr1, np.nan_to_num(arr2))


@jit(nopython=False)
def b_div(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.divide(arr1, arr2)


@jit(nopython=False)
def b_corr(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.corrcoef(arr1, arr2)


@jit(nopython=False)
def b_cov(arr1: np.array, arr2: np.array):
    arr1 = np.nan_to_num(arr1)
    arr2 = np.nan_to_num(arr2)
    return np.cov(arr1, arr2)
