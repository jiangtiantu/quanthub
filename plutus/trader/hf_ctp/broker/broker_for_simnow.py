import _thread
import re

import pandas as pd
import py_ctp.ctp_struct as ctp_struct
from py_ctp.ctp_quote import Quote
from py_ctp.ctp_trade import Trade
from py_ctp.enums import *
from py_ctp.structs import *


class BrokerCta:
    def __init__(self, account_info, instruments_sub_list):

        self.investor = account_info["user_id"]
        self.pwd = account_info["pass_word"]
        self.broker = account_info["broker_id"]
        self.authcode = account_info["auth_code"]
        self.appid = account_info["app_id"]
        self.front_md = account_info["md_fronts"]
        self.front_td = account_info["trading_fronts"]
        self.proc = "@hahaha"
        self.instruments_sub_list = instruments_sub_list
        self.data_dir = "./data/"

        self.symbol_and_exchange_df = pd.read_csv(
            f"{self.data_dir}/config/symbol_and_exchange.csv", index_col=0
        )

        self.t = Trade()
        self.q = Quote()

        self.RelogEnable = True
        self.needAuth = True

        self.instruments = {}
        self.DepthMarketDatas = {}
        self.q_tick_datas = {}

        self.req = 0
        self.existed_long_positions = {}
        self.existed_short_positions = {}
        self.order_records = {}

    # 初始化行情api
    def StartQuote(self):
        self.q.CreateApi()
        spi = self.q.CreateSpi()
        self.q.RegisterSpi(spi)
        self.q.OnFrontConnected = self.q_OnFrontConnected
        self.q.OnRspUserLogin = self.q_OnRspUserLogin
        self.q.OnRtnDepthMarketData = self.q_OnRtnDepthMarketData
        self.q.OnRspSubMarketData = self.q_OnRspSubMarketData
        self.q.RegCB()
        self.q.RegisterFront(self.front_md)
        self.q.Init()
        print(f"startQuate")

    # 初始化交易api
    def StartTrade(self):
        # 创建交易api
        self.t = Trade()
        self.t.CreateApi()
        t_spi = self.t.CreateSpi()
        self.t.RegisterSpi(t_spi)
        self.t.OnFrontConnected = self.OnFrontConnected
        self.t.OnFrontDisconnected = self.OnFrontDisconnected
        self.t.OnRspAuthenticate = self.OnRspAuthenticate
        self.t.OnRspUserLogin = self.OnRspUserLogin
        self.t.OnRspSettlementInfoConfirm = self.OnRspSettlementInfoConfirm
        self.t.OnRspQryTradingAccount = self.OnRspQryTradingAccount
        # self.t.OnRspQryInstrument = self.OnRspQryInstrument
        self.t.OnRspQryInvestorPosition = self.OnRspQryInvestorPosition
        self.t.OnRtnInstrumentStatus = self.OnRtnInstrumentStatus
        self.t.OnRtnOrder = self.OnRtnOrder
        self.t.OnRtnTrade = self.OnRtnTrade
        self.t.OnErrRtnOrderAction = self.OnErrRtnOrderAction
        self.t.OnRspOrderAction = self.OnRspOrderAction
        self.t.OnErrRtnOrderInsert = self.OnErrRtnOrderInsert

        self.t.RegCB()
        self.t.RegisterFront(self.front_td)
        self.t.SubscribePrivateTopic(nResumeType=2)
        # self.t.SubscribePublicTopic()
        self.t.Init()
        print("StartTrade")

    # 登录行情api
    def login(self):
        self.q.ReqUserLogin(
            BrokerID=self.broker, UserID=self.investor, Password=self.pwd
        )

    # 释放接口,安全退出
    def release(self):
        self.q.Release()
        self.t.Release()

    # 下单函数
    def ReqOrderInsert(
        self,
        pInstrument: str,
        pDirection: DirectType,
        pOffset: OffsetType,
        pPrice: float = 0.0,
        pVolume: int = 1,
        pType: OrderType = OrderType.Limit,
        pCustom: int = 0,
    ):

        OrderPriceType = ctp_struct.TThostFtdcOrderPriceTypeType.THOST_FTDC_OPT_AnyPrice
        TimeCondition = ctp_struct.TThostFtdcTimeConditionType.THOST_FTDC_TC_IOC
        LimitPrice = 0.0
        VolumeCondition = ctp_struct.TThostFtdcVolumeConditionType.THOST_FTDC_VC_AV

        if pType == OrderType.Market:  # 市价
            OrderPriceType = (
                ctp_struct.TThostFtdcOrderPriceTypeType.THOST_FTDC_OPT_AnyPrice
            )
            TimeCondition = ctp_struct.TThostFtdcTimeConditionType.THOST_FTDC_TC_IOC
            LimitPrice = 0.0
            VolumeCondition = ctp_struct.TThostFtdcVolumeConditionType.THOST_FTDC_VC_AV
        elif pType == OrderType.Limit:  # 限价
            OrderPriceType = (
                ctp_struct.TThostFtdcOrderPriceTypeType.THOST_FTDC_OPT_LimitPrice
            )
            TimeCondition = ctp_struct.TThostFtdcTimeConditionType.THOST_FTDC_TC_GFD
            LimitPrice = pPrice
            VolumeCondition = ctp_struct.TThostFtdcVolumeConditionType.THOST_FTDC_VC_AV
        elif pType == OrderType.FAK:  # FAK
            OrderPriceType = (
                ctp_struct.TThostFtdcOrderPriceTypeType.THOST_FTDC_OPT_LimitPrice
            )
            TimeCondition = ctp_struct.TThostFtdcTimeConditionType.THOST_FTDC_TC_IOC
            LimitPrice = pPrice
            VolumeCondition = ctp_struct.TThostFtdcVolumeConditionType.THOST_FTDC_VC_AV
        elif pType == OrderType.FOK:  # FOK
            OrderPriceType = (
                ctp_struct.TThostFtdcOrderPriceTypeType.THOST_FTDC_OPT_LimitPrice
            )
            TimeCondition = ctp_struct.TThostFtdcTimeConditionType.THOST_FTDC_TC_IOC
            LimitPrice = pPrice
            VolumeCondition = (
                ctp_struct.TThostFtdcVolumeConditionType.THOST_FTDC_VC_CV
            )  # 全部数量

        self.req += 1
        self.t.ReqOrderInsert(
            BrokerID=self.broker,
            InvestorID=self.investor,
            InstrumentID=pInstrument,
            OrderRef="%06d%06d" % (self.req, pCustom % 1000000),
            UserID=self.investor,
            # ExchangeID=self.instruments[pInstrument].getExchangeID(),
            ExchangeID=(
                self.symbol_and_exchange_df["exchange_ctp"][
                    re.sub(r"[0-9]+", "", pInstrument).upper()
                ]
            ),
            # 此处ctp_enum与at_struct名称冲突
            Direction=ctp_struct.TThostFtdcDirectionType.THOST_FTDC_D_Buy
            if pDirection == DirectType.Buy
            else ctp_struct.TThostFtdcDirectionType.THOST_FTDC_D_Sell,
            CombOffsetFlag=chr(
                ctp_struct.TThostFtdcOffsetFlagType.THOST_FTDC_OF_Open.value
                if pOffset == OffsetType.Open
                else ctp_struct.TThostFtdcOffsetFlagType.THOST_FTDC_OF_CloseToday.value
                if pOffset == OffsetType.CloseToday
                else ctp_struct.TThostFtdcOffsetFlagType.THOST_FTDC_OF_Close.value
            ),
            CombHedgeFlag=chr(
                ctp_struct.TThostFtdcHedgeFlagType.THOST_FTDC_HF_Speculation.value
            ),
            IsAutoSuspend=0,
            ForceCloseReason=ctp_struct.TThostFtdcForceCloseReasonType.THOST_FTDC_FCC_NotForceClose,
            IsSwapOrder=0,
            ContingentCondition=ctp_struct.TThostFtdcContingentConditionType.THOST_FTDC_CC_Immediately,
            VolumeCondition=VolumeCondition,
            MinVolume=1,
            VolumeTotalOriginal=pVolume,
            OrderPriceType=OrderPriceType,
            TimeCondition=TimeCondition,
            LimitPrice=LimitPrice,
        )

    # 撤单函数
    def ReqOrderAction(self, pOrder):
        return self.t.ReqOrderAction(
            BrokerID=self.broker,
            InvestorID=self.investor,
            UserID=self.investor,
            OrderSysID=pOrder.getOrderSysID(),
            ExchangeID=pOrder.getExchangeID(),
            ActionFlag=ctp_struct.TThostFtdcActionFlagType.THOST_FTDC_AF_Delete,
        )

    # 订阅行情函数
    def subscribe(self, code):
        if isinstance(code, list):
            for item in code:
                try:
                    self.q.SubscribeMarketData(item)
                except:
                    pass
        elif isinstance(code, str):
            self.subscribe([code])

    # 行情回调
    def q_OnFrontConnected(self):
        self.login()

    def q_OnRspUserLogin(
        self,
        rsp: ctp_struct.CThostFtdcRspUserLoginField,
        info: ctp_struct.CThostFtdcRspInfoField,
        req: int,
        last: bool,
    ):
        if info.getErrorID() == 0:
            print("===q_OnRspUserLogin===行情登陆成功", self.investor)
            self.subscribe(self.instruments_sub_list)
        else:
            print("===q_OnRspUserLogin===行情登陆出现了一些问题", self.investor)

    def q_OnRspSubMarketData(
        self,
        pSpecificInstrument: ctp_struct.CThostFtdcSpecificInstrumentField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        if pRspInfo.getErrorID() == 0:
            print(
                "===q_OnRspSubMarketData===行情订阅成功",
                pSpecificInstrument.getInstrumentID(),
            )
        else:
            print("===q_OnRspSubMarketData===行情订阅出现了一些问题", pSpecificInstrument)

    def q_OnRtnDepthMarketData(self, tick: ctp_struct.CThostFtdcMarketDataField):
        return

    # 交易回调
    def OnFrontConnected(self):
        if not self.RelogEnable:
            return
        if self.needAuth:
            self.t.ReqAuthenticate(
                BrokerID=self.broker,
                UserID=self.investor,
                UserProductInfo=self.proc,
                AuthCode=self.authcode,
                AppID=self.appid,
            )
        else:
            self.t.ReqUserLogin(
                BrokerID=self.broker,
                UserID=self.investor,
                Password=self.pwd,
                UserProductInfo=self.proc,
            )

    def OnFrontDisconnected(self, reason: int):
        print("不知道为什么,断开了连接")

    def OnRspAuthenticate(
        self,
        pRspAuthenticateField: ctp_struct.CThostFtdcRspAuthenticateField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        self.t.ReqUserLogin(
            BrokerID=self.broker,
            UserID=self.investor,
            UserProductInfo=self.proc,
            Password=self.pwd,
        )

    def OnRspUserLogin(
        self,
        rsp: ctp_struct.CThostFtdcRspUserLoginField,
        info: ctp_struct.CThostFtdcRspInfoField,
        req: int,
        last: bool,
    ):
        if info.getErrorID() == 0:
            self.Session = rsp.getSessionID()
            self.t.ReqSettlementInfoConfirm(
                BrokerID=self.broker, InvestorID=self.investor
            )
        else:
            self.RelogEnable = False

    def OnRspSettlementInfoConfirm(
        self,
        pSettlementInfoConfirm: ctp_struct.CThostFtdcSettlementInfoConfirmField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        self.t.ReqQryTradingAccount(self.broker, self.investor)

    def OnRspQryTradingAccount(
        self,
        pTradingAccount: ctp_struct.CThostFtdcTradingAccountField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        print(
            "===OnRspQryTradingAccount===",
            pTradingAccount.getTradingDay(),
            pTradingAccount.getAccountID(),
            pTradingAccount.getBalance(),
        )
        if bIsLast:
            # self.t.ReqQryInstrument()
            # self.t.ReqQryDepthMarketData()
            # self.t.ReqQryInvestorPosition(self.broker, self.investor)
            _thread.start_new_thread(self.StartQuote, ())

    def OnRspQryInstrument(
        self,
        pInstrument: ctp_struct.CThostFtdcInstrumentField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        self.instruments[pInstrument.getInstrumentID()] = pInstrument
        if bIsLast:
            # self.t.ReqQryDepthMarketData()
            self.t.ReqQryInvestorPosition(self.broker, self.investor)
            print("===OnRspQryInstrument=== is over")

    def OnRspQryDepthMarketData(
        self,
        pDepthMarketData: ctp_struct.CThostFtdcDepthMarketDataField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        self.DepthMarketDatas[pDepthMarketData.getInstrumentID()] = pDepthMarketData
        if bIsLast:
            self.t.ReqQryInvestorPosition(self.broker, self.investor)
            print("===OnRspQryDepthMarketData=== is over")

    def OnRspQryInvestorPosition(
        self,
        pInvestorPosition: ctp_struct.CThostFtdcInvestorPositionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):

        if pInvestorPosition.getPosition() != 0:
            if (
                pInvestorPosition.getPosiDirection()
                == ctp_struct.TThostFtdcPosiDirectionType.THOST_FTDC_PD_Long
                and ("&" not in pInvestorPosition.getInstrumentID())
            ):
                self.existed_long_positions[
                    pInvestorPosition.getInstrumentID()
                ] = pInvestorPosition.getPosition()
            if (
                pInvestorPosition.getPosiDirection()
                == ctp_struct.TThostFtdcPosiDirectionType.THOST_FTDC_PD_Short
                and ("&" not in pInvestorPosition.getInstrumentID())
            ):
                self.existed_short_positions[
                    pInvestorPosition.getInstrumentID()
                ] = pInvestorPosition.getPosition()
        if bIsLast:
            print("===OnRspQryInvestorPosition=== is over")
            _thread.start_new_thread(self.StartQuote, ())

    def OnRtnInstrumentStatus(
        self, pInstrumentStatus: ctp_struct.CThostFtdcInstrumentStatusField
    ):
        # print('===OnRtnInstrumentStatus===: pInstrumentStatus: CThostFtdcInstrumentStatusField')
        # print(pInstrumentStatus)
        return

    def OnRspOrderInsert(
        self,
        pInputOrder: ctp_struct.CThostFtdcInputOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        print("===OnRspOrderInsert===", pInputOrder)

    def OnRspQryOrder(
        self,
        pOrder: ctp_struct.CThostFtdcOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        print("===OnRspQryOrder===", pOrder)

    def OnRtnOrder(self, pOrder: ctp_struct.CThostFtdcOrderField):
        return

    def OnRtnTrade(self, pTrade: ctp_struct.CThostFtdcTradeField):
        return
        # print('===OnRtnTrade===:', pTrade)

    def OnErrRtnOrderInsert(
        self,
        pInputOrder: ctp_struct.CThostFtdcInputOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
    ):
        print("===OnErrRtnOrderInsert===", pInputOrder, pRspInfo)

    def OnRspOrderAction(
        self,
        pInputOrderAction: ctp_struct.CThostFtdcInputOrderActionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        print("===OnRspOrderAction===", pInputOrderAction, pRspInfo)

    def OnErrRtnOrderAction(
        self,
        pOrderAction: ctp_struct.CThostFtdcOrderActionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
    ):
        print("===OnErrRtnOrderAction===", pOrderAction, pRspInfo)
