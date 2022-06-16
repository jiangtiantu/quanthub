import pandas as pd


def resample_md(
    df: pd.DataFrame,
    target_timeframe: str,
    label_at: str = "right",
    close_at: str = "right",
):
    """
    to resample higher granular md data into lower granular md data
    :param df:  source dataframe
    :param target_timeframe:  timeframe to which you want to transform source dataframe
    :param label_at: where to extract your target data label. 'right' by default
    :param close_at: where to extract your target data from sample bins, 'right' by default
    :return: resampled dataframe
    """
    target_df = (
        df[["open"]].resample(target_timeframe, label=label_at, closed=close_at).first()
    )
    target_df["high"] = (
        df["high"].resample(target_timeframe, label=label_at, closed=close_at).max()
    )
    target_df["low"] = (
        df["low"].resample(target_timeframe, label=label_at, closed=close_at).min()
    )
    if "close" in df.columns:
        target_df["close"] = (
            df["close"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .last()
        )
    if "last" in df.columns:
        target_df["last"] = (
            df["last"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .last()
        )
    if "pre_close" in df.columns:
        target_df["pre_close"] = (
            df["pre_close"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .first()
        )
    if "volume" in df.columns:
        target_df["volume"] = (
            df["volume"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .sum()
        )
    if "turnover" in df.columns:
        target_df["turnover"] = (
            df["turnover"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .sum()
        )
    if "open_interest" in df.columns:
        target_df["open_interest"] = (
            df["open_interest"]
            .resample(target_timeframe, label=label_at, closed=close_at)
            .sum()
        )
    return target_df
