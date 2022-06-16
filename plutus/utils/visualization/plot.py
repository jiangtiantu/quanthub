import matplotlib.pyplot as plt


class PlotTS:
    @staticmethod
    def plot_cumsum_pnl(master_data):
        """

        :param master_data:
        :return:
        """
        master_data["pnl_period_cumsum"].plot()
        plt.show()


class PlotCS:
    @staticmethod
    def plot_group_cumsum_pnl(
        clean_factor_data, groupby_col: list = ["trading_date", "factor_quantile"]
    ):
        """

        :param clean_factor_data:
        :return:
        """
        df_factor_quantile = (
            clean_factor_data.reset_index()
            .groupby(groupby_col)["period"]
            .mean()
            .unstack()
            .cumsum()
        )
        df_factor_quantile.plot(figsize=(16, 9), title="test")
        plt.show()

    def plot_long_short_cumsum_pnl(self, clean_factor_data):
        pass
