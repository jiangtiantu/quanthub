import _thread
import string
import time

import pandas as pd
import py_ctp.ctp_struct as ctp_struct
from py_ctp.ctp_quote import Quote
from py_ctp.ctp_trade import Trade
from py_ctp.enums import *
from py_ctp.structs import *


class BrokerCTP:
    def __init__(self, account_info):

        self.investor = account_info["user_id"]
        self.pwd = account_info["pass_word"]
        self.broker = account_info["broker_id"]
        self.authcode = account_info["auth_code"]
        self.appid = account_info["app_id"]
        self.front_md = account_info["md_fronts"]
        self.front_td = account_info["trading_fronts"]
        self.proc = "@jtt"
        self.symbol_info = pd.read_parquet(
            "../../../datahub/raw/cn/future/master/symbol_info.parquet"
        )
        self.symbol_info.set_index("symbol", inplace=True)
        self.instrument_dict = self.symbol_info["exchange_ctp"].to_dict()
        self.can_trade_instrument_dict = {}

        self.t = Trade()
        self.q = Quote()

        self.RelogEnable = True
        self.needAuth = True
        self.isqryposition = False
        self.isubscribed = False

        # self.instrument_dict = {}
        self.DepthMarketData_dict = {}
        self.q_tick_data_dict = {}

        self.req = 0
        self.existed_long_position_dict = {}
        self.existed_short_position_dict = {}
        self.order_record_dict = {}

    def StartQuote(self):
        """
        创建行情api
        :return:
        """
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

    def StartTrade(self):
        """
        创建交易api
        :return:
        """
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
        self.t.OnRspQryInstrument = self.OnRspQryInstrument
        self.t.OnRspQryInvestorPosition = self.OnRspQryInvestorPosition
        self.t.OnRtnInstrumentStatus = self.OnRtnInstrumentStatus
        self.t.OnRspError = self.OnRspError
        self.t.RegCB()
        self.t.RegisterFront(self.front_td)
        self.t.SubscribePrivateTopic(nResumeType=2)

        self.t.Init()
        print("StartTrade")

    # 登录行情api
    def login(self):
        """
        登录行情api
        :return:
        """
        self.q.ReqUserLogin(
            BrokerID=self.broker, UserID=self.investor, Password=self.pwd
        )

    def release(self):
        """
        释放接口,安全退出
        :return:
        """
        self.q.Release()
        self.t.Release()

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
        """
        下单函数
        :param pInstrument:
        :param pDirection:
        :param pOffset:
        :param pPrice:
        :param pVolume:
        :param pType:
        :param pCustom:
        :return:
        """
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
            # ExchangeID=self.instrument_dict[pInstrument.rstrip(string.digits)].getExchangeID(),
            ExchangeID=self.instrument_dict[pInstrument.rstrip(string.digits).upper()],
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

    def ReqOrderAction(self, OrderSysID: str = ""):
        """
        撤单函数
        :param OrderSysID:
        :return:
        """
        return self.t.ReqOrderAction(
            BrokerID=self.broker,
            InvestorID=self.investor,
            UserID=self.investor,
            OrderSysID=OrderSysID,
            ExchangeID=self.order_record_dict[OrderSysID].getExchangeID(),
            ActionFlag=ctp_struct.TThostFtdcActionFlagType.THOST_FTDC_AF_Delete,
        )

    def subscribe(self, code):
        """
        订阅行情函数
        :param code:
        :return:
        """
        if isinstance(code, list):
            for item in code:
                try:
                    self.q.SubscribeMarketData(item)
                except:
                    pass
        elif isinstance(code, str):
            self.subscribe([code])

    def q_OnFrontConnected(self):
        self.login()

    def q_OnRspUserLogin(
        self,
        rsp: ctp_struct.CThostFtdcRspUserLoginField,
        info: ctp_struct.CThostFtdcRspInfoField,
        req: int,
        last: bool,
    ):
        """
        行情回调
        :param rsp:
        :param info:
        :param req:
        :param last:
        :return:
        """
        if info.getErrorID() == 0:
            print("===q_OnRspUserLogin===行情登陆成功", self.investor)
        else:
            print("===q_OnRspUserLogin===行情登陆出现了一些问题", self.investor)

    def q_OnRspSubMarketData(
        self,
        pSpecificInstrument: ctp_struct.CThostFtdcSpecificInstrumentField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        订阅回调
        :param pSpecificInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        if pRspInfo.getErrorID() == 0:
            print(
                f"===q_OnRspSubMarketData===行情订阅成功{pSpecificInstrument}",
            )
        else:
            print("===q_OnRspSubMarketData===行情订阅出现了一些问题", pSpecificInstrument)

    def q_OnRtnDepthMarketData(self, tick: ctp_struct.CThostFtdcMarketDataField):
        self.q_tick_data_dict[tick.getInstrumentID()] = tick

    def OnFrontConnected(self):
        """
        当客户端与交易后台建立起通信连接时（还未登录前）,该方法被调用。
        :return:
        """
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
        """
        当客户端与交易后台通信连接断开时,该方法被调用。当发生这个情况后,API会自动重新连接,客户端可不做处理。
        :param reason:
        :return:
        """
        print("不知道为什么,断开了连接")

    def OnRspAuthenticate(
        self,
        pRspAuthenticateField: ctp_struct.CThostFtdcRspAuthenticateField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        登录认证
        :param pRspAuthenticateField:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
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
        """
        登录回调
        :param rsp:
        :param info:
        :param req:
        :param last:
        :return:
        """
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
        """
        确认结算信息
        :param pSettlementInfoConfirm:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        self.t.ReqQryTradingAccount(self.broker, self.investor)

    def OnRspQryTradingAccount(
        self,
        pTradingAccount: ctp_struct.CThostFtdcTradingAccountField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        查询账户回调
        :param pTradingAccount:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        print(
            "===OnRspQryTradingAccount===",
            pTradingAccount.getTradingDay(),
            pTradingAccount.getAccountID(),
            pTradingAccount.getBalance(),
        )
        if bIsLast:
            # pass
            # _thread.start_new_thread(self.StartQuote, ())
            # self.t.ReqQryInstrument()
            # self.t.ReqQryDepthMarketData()
            time.sleep(3)
            self.t.ReqQryInvestorPosition(self.broker, self.investor)

    def OnRspQryInstrument(
        self,
        pInstrument: ctp_struct.CThostFtdcInstrumentField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        查询合约回调
        :param pInstrument:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        pass

        # self.instrument_dict[pInstrument.getInstrumentID()] = pInstrument

        if bIsLast:
            # self.t.ReqQryDepthMarketData()
            self.t.ReqQryInvestorPosition(self.broker, self.investor)

            print("===OnRspQryInstrument=== is over")
        else:
            print("===OnRspQryInstrument===", pInstrument.getInstrumentID())

    def OnRspQryDepthMarketData(
        self,
        pDepthMarketData: ctp_struct.CThostFtdcDepthMarketDataField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        查询行情回调
        :param pDepthMarketData:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        self.DepthMarketData_dict[pDepthMarketData.getInstrumentID()] = pDepthMarketData
        if bIsLast:
            self.t.ReqQryInvestorPosition(self.broker, self.investor)
            print("===OnRspQryDepthMarketData=== is over")
        else:
            print("===OnRspQryDepthMarketData===", pDepthMarketData.getInstrumentID())

    def OnRspQryInvestorPosition(
        self,
        pInvestorPosition: ctp_struct.CThostFtdcInvestorPositionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        查询持仓回调
        :param pInvestorPosition:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        if pInvestorPosition.getPosition() != 0:
            if (
                pInvestorPosition.getPosiDirection()
                == ctp_struct.TThostFtdcPosiDirectionType.THOST_FTDC_PD_Long
                and ("&" not in pInvestorPosition.getInstrumentID())
            ):
                self.existed_long_position_dict[
                    pInvestorPosition.getInstrumentID()
                ] = pInvestorPosition.getPosition()
            if (
                pInvestorPosition.getPosiDirection()
                == ctp_struct.TThostFtdcPosiDirectionType.THOST_FTDC_PD_Short
                and ("&" not in pInvestorPosition.getInstrumentID())
            ):
                self.existed_short_position_dict[
                    pInvestorPosition.getInstrumentID()
                ] = pInvestorPosition.getPosition()
        if bIsLast:
            print("===OnRspQryInvestorPosition=== is over")
            self.isqryposition = True
            _thread.start_new_thread(self.StartQuote, ())
        else:
            print("===OnRspQryInvestorPosition===", pInvestorPosition.getInstrumentID())

    def OnRspOrderInsert(
        self,
        pInputOrder: ctp_struct.CThostFtdcInputOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        下单回调
        :param pInputOrder:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        print("===OnRspOrderInsert===", pInputOrder)

    def OnRspQryOrder(
        self,
        pOrder: ctp_struct.CThostFtdcOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        查询订单回调
        :param pOrder:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        print("===OnRspQryOrder===", pOrder)

    def OnRtnOrder(self, pOrder: ctp_struct.CThostFtdcOrderField):
        """
        报单回调
        :param pOrder:
        :return:
        """
        if pOrder.getOrderSysID() != "" and pOrder.getStatusMsg() != "已撤单":
            self.order_record_dict[pOrder.getOrderSysID()] = pOrder

        if pOrder.getStatusMsg() == "已撤单":
            self.order_record_dict.pop(pOrder.getOrderSysID())
            if (
                pOrder.getDirection()
                == ctp_struct.TThostFtdcDirectionType.THOST_FTDC_D_Buy
            ):
                self.ReqOrderInsert(
                    pInstrument=pOrder.getInstrumentID(),
                    pDirection=DirectType.Buy,
                    pOffset=OffsetType(int(pOrder.getCombOffsetFlag())),
                    pPrice=self.q_tick_data_dict[
                        pOrder.getInstrumentID()
                    ].getBidPrice1(),
                    pVolume=int(
                        pOrder.getVolumeTotalOriginal() - pOrder.getVolumeTraded()
                    ),
                )
            if (
                pOrder.getDirection()
                == ctp_struct.TThostFtdcDirectionType.THOST_FTDC_D_Sell
            ):
                self.ReqOrderInsert(
                    pInstrument=pOrder.getInstrumentID(),
                    pDirection=DirectType.Sell,
                    pOffset=OffsetType(int(pOrder.getCombOffsetFlag())),
                    pPrice=self.q_tick_data_dict[
                        pOrder.getInstrumentID()
                    ].getAskPrice1(),
                    pVolume=int(
                        pOrder.getVolumeTotalOriginal() - pOrder.getVolumeTraded()
                    ),
                )

        if pOrder.getStatusMsg() == "全部成交":
            self.order_record_dict.pop(pOrder.getOrderSysID())

    def OnErrRtnOrderInsert(
        self,
        pInputOrder: ctp_struct.CThostFtdcInputOrderField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
    ):
        """
        下单错误回调
        :param pInputOrder:
        :param pRspInfo:
        :return:
        """
        print("===OnErrRtnOrderInsert===:", pInputOrder, pRspInfo)

    def OnRspOrderAction(
        self,
        pInputOrderAction: ctp_struct.CThostFtdcInputOrderActionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """
        撤单回调
        :param pInputOrderAction:
        :param pRspInfo:
        :param nRequestID:
        :param bIsLast:
        :return:
        """
        print("===OnRspOrderAction===: ", pInputOrderAction, pRspInfo)

    def OnErrRtnOrderAction(
        self,
        pOrderAction: ctp_struct.CThostFtdcOrderActionField,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
    ):
        """
        撤单错误回调
        :param pOrderAction:
        :param pRspInfo:
        :return:
        """
        print("===OnErrRtnOrderAction===: ", pOrderAction, pRspInfo)

    def OnRtnTrade(self, pTrade: ctp_struct.CThostFtdcTradeField):
        """
        成交回调
        :param pTrade:
        :return:
        """
        # print('===OnRtnTrade===:', pTrade)
        # self.order_record_dict[pTrade.getOrderSysID()]=self.order_record_dict[pTrade.getOrderSysID()]-pTrade.getVolume()
        return

    def OnRtnInstrumentStatus(
        self, pInstrumentStatus: ctp_struct.CThostFtdcInstrumentStatusField
    ):
        self.can_trade_instrument_dict[pInstrumentStatus.getInstrumentID()] = [
            pInstrumentStatus.getInstrumentStatus(),
            pInstrumentStatus.getEnterTime(),
        ]

    def OnRspError(
        self,
        pRspInfo: ctp_struct.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        print("===OnRspError===: ", pRspInfo, nRequestID, bIsLast)

    def OnRtnForQuoteRsp(self, pForQuoteRsp: ctp_struct.CThostFtdcForQuoteRspField):
        print(pForQuoteRsp)
