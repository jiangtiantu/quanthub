import json
import string
from datetime import datetime
from time import sleep

import numpy as np
import pandas as pd
from py_ctp.enums import *

from plutus.trader.hf_ctp.broker.broker_ctp import BrokerCTP


class CtpScan(BrokerCTP):
    def __init__(self, account: str):
        with open("config/account_info.json", "r") as f:
            account_dict = json.load(f)
        account_info = account_dict[account]
        super(CtpScan, self).__init__(account_info)
        self.position_dir = f"../../../positionhub/"
        self.account = account

    def get_instrument_info(self, instrument_id: str):
        pass

    def get_target_position(self, position_dir: str):
        target_position_df = pd.read_csv(
            f"{position_dir}{self.account}/target_position/{datetime.now().strftime('%Y-%m-%d')}.csv",
        )
        target_position_df.set_index(["contract"], inplace=True)
        target_position_s = target_position_df["ss"]
        target_long_position_s = (target_position_s[target_position_s > 0]).dropna()
        target_short_position_s = (
            abs(target_position_s[target_position_s < 0])
        ).dropna()

        return (
            target_position_s,
            target_long_position_s,
            target_short_position_s,
        )

    def get_existed_position(self):
        return pd.Series(self.existed_long_position_dict), pd.Series(
            self.existed_short_position_dict
        )

    def get_trade_position(
        self,
        target_long_position_s,
        target_short_position_s,
        existed_long_position_s,
        existed_short_position_s,
    ):
        long_trade_s = (
            target_long_position_s.sub(existed_long_position_s, fill_value=0)
            .replace([0], np.nan)
            .dropna()
        )
        short_trade_s = (
            target_short_position_s.sub(existed_short_position_s, fill_value=0)
            .replace([0], np.nan)
            .dropna()
        )
        return long_trade_s, short_trade_s

    def run(self):
        self.StartTrade()
        (
            target_position_s,
            target_long_position_s,
            target_short_position_s,
        ) = self.get_target_position(self.position_dir)
        while 1:
            if self.isqryposition:
                (
                    existed_long_position_s,
                    existed_short_position_s,
                ) = self.get_existed_position()
                break
            sleep(1)

        print(
            f"{self.account} existed_long_position_s: {existed_long_position_s}, existed_short_position_s: {existed_short_position_s}"
        )
        long_trade_s, short_trade_s = self.get_trade_position(
            target_long_position_s,
            target_short_position_s,
            existed_long_position_s,
            existed_short_position_s,
        )

        trading_code_list = list(
            set(list(long_trade_s.index) + list(short_trade_s.index))
        )
        if datetime.now().hour > 18 or datetime.now().hour < 9:
            trading_code_list = [
                i
                for i in trading_code_list
                if i.rstrip(string.digits)
                not in [
                    "IF",
                    "IH",
                    "IC",
                    "TF",
                    "T",
                    "TS",
                    "PK",
                    "UR",
                    "WH",
                    "UR",
                    "SM",
                    "SF",
                    "CJ",
                    "AP",
                    "RI",
                    "JR",
                    "lu",
                    "jd",
                ]
            ]
            long_trade_s = long_trade_s.loc[
                (long_trade_s.index.isin(trading_code_list))
            ]
            short_trade_s = short_trade_s.loc[
                (short_trade_s.index.isin(trading_code_list))
            ]

        self.subscribe(trading_code_list)

        while 1:
            if len(set(self.q_tick_data_dict.keys())) >= len(set(trading_code_list)):
                break
            else:
                print(self.q_tick_data_dict)
                print("collect tick data ,please waiting")
                sleep(0.1)

        while 1:
            if datetime.now().hour >= 21 or (9 <= datetime.now().hour < 15):
                break
            else:
                sleep(1)

        for contract in long_trade_s.index:
            position_diff = long_trade_s[contract]

            if (position_diff) < 0:
                self.ReqOrderInsert(
                    pInstrument=contract,
                    pDirection=DirectType.Sell,
                    pOffset=OffsetType.Close,
                    # pPrice=self.q_tick_data_dict[contract].getAskPrice1(),
                    pPrice=self.q_tick_data_dict[contract].getBidPrice1(),
                    pVolume=int(abs(position_diff)),
                )

            if (position_diff) > 0:
                self.ReqOrderInsert(
                    pInstrument=contract,
                    pDirection=DirectType.Buy,
                    pOffset=OffsetType.Open,
                    # pPrice=self.q_tick_data_dict[contract].getBidPrice1(),
                    pPrice=self.q_tick_data_dict[contract].getAskPrice1(),
                    pVolume=int(abs(position_diff)),
                )

        for contract in short_trade_s.index:
            position_diff = short_trade_s[contract]
            if (position_diff) < 0:
                self.ReqOrderInsert(
                    pInstrument=contract,
                    pDirection=DirectType.Buy,
                    pOffset=OffsetType.Close,
                    # pPrice=self.q_tick_data_dict[contract].getBidPrice1(),
                    pPrice=self.q_tick_data_dict[contract].getAskPrice1(),
                    pVolume=int(abs(position_diff)),
                )

            if (position_diff) > 0:
                self.ReqOrderInsert(
                    pInstrument=contract,
                    pDirection=DirectType.Sell,
                    pOffset=OffsetType.Open,
                    # pPrice=self.q_tick_data_dict[contract].getAskPrice1(),
                    pPrice=self.q_tick_data_dict[contract].getBidPrice1(),
                    pVolume=int(abs(position_diff)),
                )

        cancel_order_num = 0

        while 1:
            if cancel_order_num < 200:
                sleep(10.1)
                order_records = {
                    k: v
                    for k, v in self.order_record_dict.items()
                    if v.getVolumeTotal() >= 0
                }
                if len(order_records.keys()) == 0:
                    print("all order is over,stop trading,save position")
                    self.t.ReqQryInvestorPosition(self.broker, self.investor)
                    sleep(5)
                    break
                elif len(order_records.keys()) > 0:
                    for k, v in order_records.items():
                        self.ReqOrderAction(k)
                        cancel_order_num = cancel_order_num + 1
                else:
                    print("error warning")
            else:
                print("撤单次数超过200次")
                break

        self.t.Release()
        self.q.Release()


if __name__ == "__main__":
    ctp_scan = CtpScan(account="simnow")
    ctp_scan.run()
