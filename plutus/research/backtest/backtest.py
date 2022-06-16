import empyrical as ep
import numpy as np
import pandas as pd

from plutus.utils.visualization.plot import PlotTS


class Backtest:
    def __init__(self):
        pass

    @staticmethod
    def clip_returns_to_benchmark(rets, benchmark_rets):
        """
        将净值收益和benchmark对齐
        :param rets:
        :param benchmark_rets:
        :return:
        """
        if (rets.index[0] < benchmark_rets.index[0]) or (
            rets.index[-1] > benchmark_rets.index[-1]
        ):
            clipped_rets = rets[benchmark_rets.index]
        else:
            clipped_rets = rets
        return clipped_rets

    @staticmethod
    def performance_stats(returns: pd.Series):
        """
        输出净值的指标合集,年化收益,累计收益,年华波动率,夏普率,卡玛比率,最大回撤
        :param returns:
        :return:
        """

        simple_stat_funcs = [
            ep.annual_return,
            ep.cum_returns_final,
            ep.annual_volatility,
            ep.sharpe_ratio,
            ep.calmar_ratio,
            ep.max_drawdown,
        ]

        stats = pd.Series()
        for stat_func in simple_stat_funcs:
            stats[stat_func.__name__] = stat_func(returns)
        return stats

    @staticmethod
    def cal_correct_radio(forecast_result):
        """
        计算交易信号的正确率
        :param forecast_result:
        :return:
        """
        forecast_result.reset_index(drop=True, inplace=True)
        p_win = sum(forecast_result[forecast_result == 1]) / sum(abs(forecast_result))
        return p_win

    @staticmethod
    def stop_pnl(series: pd.Series, stop_value: int = 5):
        """
        止盈函数
        :param series:
        :param stop_value:
        :return:
        """
        signal_list = []
        trade_price = series.iloc[0]
        for i in series.iteritems():
            value = i[1]
            if value >= trade_price + stop_value:
                signal_list.append(1)
                trade_price = value
            elif value <= trade_price - stop_value:
                signal_list.append(-1)
                trade_price = value
            else:
                signal_list.append(np.nan)

        signal_s = pd.Series(signal_list)
        return signal_s

    @staticmethod
    def dynamic_stop_pnl(series: pd.Series, stop_value: int = 5):
        """
        动态止盈
        :param series:
        :param stop_value:
        :return:
        """
        signal_list = []
        trade_price = series.iloc[0]
        for i in series.iteritems():
            idx = i[0]
            value = i[1]
            if value >= trade_price + stop_value:
                signal_list.append(1)
                trade_price = value
            elif value <= trade_price - stop_value:
                signal_list.append(-1)
                trade_price = value
            else:
                signal_list.append(np.nan)
        signal_s = pd.Series(signal_list)
        last_signal = np.nan
        for signal in signal_list:
            if signal != last_signal:
                print(signal)

        return signal_s


class BacktestTS(Backtest):
    def __init__(self):
        super().__init__()

    def backtest_ts_vector_01(self, master_data: pd.DataFrame, signal: pd.Series):
        """
        向量化回测时序类策略,日频
        :param master_data: 日行情数据
        :param signal: 交易信号
        :return: 交易记录
        """
        # close_diff=master_data["close"].diff()
        close_diff = master_data["close"] - master_data["pre_close"]
        pnl_period = close_diff * signal.shift()
        pnl_period_cumsum = pnl_period.cumsum()
        master_data["signal"] = signal
        master_data["pnl_period"] = pnl_period
        master_data["pnl_period_cumsum"] = pnl_period_cumsum
        return master_data

    def backtest_ts_vector_02(self, master_data, signal):
        pass

    def backtest_ts_vector_03(self, master_data, signal):
        pass

    def describer(self, master_data):
        PlotTS.plot_cumsum_pnl(master_data=master_data)


class BacktestCS(Backtest):
    def __init__(self):
        super().__init__()

    def cal_factor_rank(
        self,
        master_data: pd.DataFrame,
        test_factor: pd.DataFrame,
    ):
        """
        将因子数据,只排序,不分组
        :param master_data:包含trading_date,code,profit 的一个dataframe
        :param test_factor:因子数据,一个dtaframe
        :return:只排序,不分组的clean_factor_data
        """
        test_factor = test_factor.replace([np.inf, -np.inf], np.nan)
        clean_factor_data = master_data.copy()
        input_factor = test_factor.copy().stack()
        clean_factor_data["factor"] = input_factor
        clean_factor_data = clean_factor_data.dropna()
        clean_factor_data["factor_rank"] = (
            clean_factor_data["factor"]
            .groupby(level=0)
            .apply(lambda x: x.rank(method="first"))
        )

        return clean_factor_data

    def cal_factor_quantile(self, clean_factor_data: pd.DataFrame, group_num):
        """
        计算因子分组
        :param clean_factor_data: 整理好的因子数据
        :param group_num: 分组数量
        :return: 一个包含factor_quantitle的dataframe
        """

        clean_factor_data["factor_quantile"] = (
            clean_factor_data["factor_rank"]
            .groupby(level=0)
            .apply(
                lambda x: (
                    (
                        pd.qcut(
                            x,
                            group_num,
                            labels=False,
                            duplicates="drop",
                        )
                        + 1
                    )
                )
            )
        )
        return clean_factor_data

    def cal_portfolio_weight(self, portfolio_data: pd.DataFrame):
        """
        计算因子权重
        :param portfolio_data:最后的持仓组合
        :return:一个dataframe
        """
        portfolio_data["factor_weight"] = (
            portfolio_data["factor_rank"] / portfolio_data["factor_rank"].sum()
        )
        return portfolio_data

    def cal_hold_portfolio(self, clean_factor_data: pd.DataFrame, hold_num: int):
        """
        计算持仓组合
        :param portfolio_data:
        :return:
        """
        long_portfolio_data = clean_factor_data.groupby(level=0).apply(
            lambda x: x[
                x["factor_quantile"] >= x["factor_quantile"].max() - (hold_num - 1)
            ].droplevel(0)
        )
        short_portfolio_data = clean_factor_data[
            clean_factor_data["factor_quantile"] <= hold_num
        ]
        return long_portfolio_data, short_portfolio_data

    def backtest_cs_vector_01(
        self,
        master_data: pd.DataFrame,
        test_factor: pd.DataFrame,
        group_num: int = 2,
    ):
        """
        向量化回测界面类策略,日频,对因子数据排序并分组
        :param master_data:包含trading_date,code,profit 的一个dataframe
        :param test_factor: 因子数据,一个dtaframe
        :param group_num: 将标的按照因子数据,分为group_num 组
        :return: clean_factor_data 一个整理好的multi_index dataframe
        """
        clean_factor_data1 = self.cal_factor_rank(master_data, test_factor)
        clean_factor_data2 = self.cal_factor_quantile(clean_factor_data1, group_num)
        return clean_factor_data2

    def describer_01(
        self,
        long_portfolio_data: pd.DataFrame,
        short_portfolio_data: pd.DataFrame,
        fee: float = 0,
    ):
        long_group_return = long_portfolio_data["period"].groupby(level=0).mean() - fee
        short_group_return = (
            short_portfolio_data["period"].groupby(level=0).mean() - fee
        )
        hedged_rate_of_return = (long_group_return - short_group_return) / 2 - fee

        long_cum_return = 1 + long_group_return.cumsum()
        short_cum_return = 1 + short_group_return.cumsum()
        hedged_cum_return = 1 + hedged_rate_of_return.cumsum()

        ret_df = pd.concat(
            [long_cum_return, short_cum_return, hedged_cum_return],
            axis=1,
        )
        ret_df.columns = ["long", "short", "long-short"]
        sharpe_ratio = ep.sharpe_ratio(
            hedged_rate_of_return, risk_free=0, period="daily", annualization=None
        )

        annual_return = ep.annual_return(hedged_rate_of_return)
        max_down = ep.max_drawdown(hedged_rate_of_return)
        ret_df = ret_df.dropna()
        return ret_df, sharpe_ratio, annual_return, max_down
