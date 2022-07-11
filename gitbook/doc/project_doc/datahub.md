# **datahub 简介**

datahub 是一个基于 Python 的金融数据工具包。提供落地历史数据库和实时数据。

**目前数据的获取有两种方案：**
- 直接通过网盘下载,数据放在datahub目录中，适合只是做点尝试和测试的同学
- 通过 Rsync 从远程服务器拉取数据,定时同步数据(只面向参与项目共建的小伙伴和付费用户)

**研究数据下载地址：**

- 链接: https://pan.baidu.com/s/1nCZIXFtG7Hoe7OvXs1uknA?pwd=n2ru 提取码: n2ru 

- 数据存储格式为parquet，使用方式请查看pyarrow 或者 researchub 中的案例。

**实时交易数据：**

- 如有需求，请小窗联系，email:qiwu12@qq.com

## **datahub 提供的每日更新的数据包括：**

# 期货数据
| 国家和地区 | 市场   | 分类   | 表名               | 释义                     | 更新频率                      |
| :--------- | :----- | :----- | :----------------- | :----------------------- | :---------------------------- |
| cn         | future | master | trading_date_info  | 国内期货交易日信息       | 每天下午6点更新上一交易日数据 |
| cn         | future | master | symbol_info        | 国内期货交易品种信息     | 每天下午6点更新上一交易日数据 |
| cn         | future | master | contract_info      | 国内期货合约信息         | 每天下午6点更新上一交易日数据 |
| cn         | future | md     | main_roll_calendar | 国内期货主力合约日历     | 每天下午6点更新上一交易日数据 |
| cn         | future | md     | all_1d             | 国内期货日行情           | 每天下午6点更新上一交易日数据 |
| cn         | future | md     | all_1m             | 国内期货分钟行情         | 每天下午6点更新上一交易日数据 |
| cn         | future | md     | main_1m            | 国内期货主力合约分钟行情 | 每天下午6点更新上一交易日数据 |
| cn         | future | md     | main_1d            | 国内期货主力合约日行情   | 每天下午6点更新上一交易日数据 |

# 股票数据

| 国家和地区 | 市场  | 分类   | 表名                       | 释义                     | 更新频率                      |
| :--------- | :---- | :----- | :------------------------- | :----------------------- | :---------------------------- |
| cn         | stock | master | code_info                  | 国内股票基础证券信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | master | share_holder_info          | 国内股票股东信息         | 每天下午6点更新上一交易日数据 |
| cn         | stock | master | share_capital_info         | 国内股票股本信息         | 每天下午6点更新上一交易日数据 |
| cn         | stock | master | allotment_info             | 国内股票分红信息         | 每天下午6点更新上一交易日数据 |
| cn         | stock | master | industry_info              | 国内股票行业分类信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | md     | all_1d                     | 国内股票日行情信息       | 每天下午6点更新上一交易日数据 |
| cn         | stock | md     | adjust_factor              | 国内股票复权因子信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | md     | all_1m                     | 国内股票分钟行情信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | index  | weight_info                | 国内股票指数权重信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | trade  | margin_info                | 国内股票融资融券信息     | 每天下午6点更新上一交易日数据 |
| cn         | stock | trade  | stock_connect_hold_info    | 国内股票北向资金持仓信息 | 每天下午6点更新上一交易日数据 |
| cn         | stock | trade  | stock_connect_balance_info | 国内股票北向资金余额信息 | 每天下午6点更新上一交易日数据 |