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

## 国内数据：

### 期货数据/future

#### 主数据/master
##### 交易日信息/trading_date_info


| 字段         | 数据类型      | 含义   |
| :----------- | ------------- | ------ |
| trading_date | DateTime64(3) | 交易日 |

```python
      
```
  
##### 商品信息/symbol_info
       
| 字段          | 数据类型 | 含义               |
| ------------- | -------- | ------------------ |
| symbol        | String   | 交易品种           |
| multiplier    | Int64    | 合约乘数           |
| exchange_tq   | String   | 天勤交易所合约代码 |
| exchange_ctp  | String   | ctp交易所合约代码  |

```python
  
```

##### 合约信息/contract_info
       
| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ---------- |
| contract       | String        | 合约名称   |
| symbol         | String        | 交易品种   |
| exchange       | String        | 交易所代码 |
| multiplier     | Float64       | 合约乘数   |
| trading_hour   | String        | 交易时间段 |
| listing_date   | DateTime64(3) | 上市日期   |
| delisting_date | DateTime64(3) | 退市日期   |

       
```python


```
       

#### 行情数据/md

##### 日行情数据/all_1d

     
| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ---------- |
| trading_date   | DateTime64(3) | 交易日     |
| symbol         | String        | 交易品种   |
| contract       | String        | 合约名称   |
| open_interest  | Float64       | 持仓量     |
| close          | Float64       | 收盘价     |
| open           | Float64       | 开盘价     |
| turnover       | Float64       | 成交额     |
| pre_settlement | Float64       | 昨日结算价 |
| settlement     | Float64       | 结算价     |
| down_limit     | Float64       | 跌停价     |
| high           | Float64       | 最高价     |
| up_limit       | Float64       | 涨停价     |
| volume         | Float64       | 成交量     |
| low            | Float64       | 最低价     |
| pre_close      | Float64       | 昨日收盘价 |
     

```python
  
```

##### 主力合约切换表/main_roll_calendar
     
| 字段         | 数据类型      | 含义                                                         |
| ------------ | ------------- | ------------------------------------------------------------ |
| trading_date | DateTime64(3) | 交易日                                                       |
| symbol       | String        | 交易品种                                                     |
| o_m          | String        | 当日主力合约,按照持仓量最大选择,单调,切换主力合约后,不再考虑旧主力合约 |
| o_nm         | String        | 当日主力合约,按照持仓量最大选择,非单调,切换主力合约后,仍然考虑旧主力合约 |
| v_m          | String        | 当日主力合约,按照成交量最大选择,单调,切换主力合约后,不再考虑旧主力合约 |
| v_nm         | String        | 当日主力合约,按照成交量最大选择,非单调,切换主力合约后,仍然考虑旧主力合约 |

     
```python
  
```
##### 切片行情数据/throttled_data
###### 30分钟数据/all_30m

| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ---------- |
| trading_date   | DateTime64(3) | 交易日     |
| symbol         | String        | 交易品种   |
| contract       | String        | 合约名称   |
| open_interest  | Float64       | 持仓量     |
| close          | Float64       | 收盘价     |
| open           | Float64       | 开盘价     |
| turnover       | Float64       | 成交额     |
| volume         | Float64       | 成交量     |
| low            | Float64       | 最低价     |


```python
  
```
###### 5分钟数据/all_5m

| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ---------- |
| trading_date   | DateTime64(3) | 交易日     |
| symbol         | String        | 交易品种   |
| contract       | String        | 合约名称   |
| open_interest  | Float64       | 持仓量     |
| close          | Float64       | 收盘价     |
| open           | Float64       | 开盘价     |
| turnover       | Float64       | 成交额     |
| volume         | Float64       | 成交量     |
| low            | Float64       | 最低价     |


```python
  
```
###### 1分钟数据/all_1m

| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ---------- |
| trading_date   | DateTime64(3) | 交易日     |
| symbol         | String        | 交易品种   |
| contract       | String        | 合约名称   |
| open_interest  | Float64       | 持仓量     |
| close          | Float64       | 收盘价     |
| open           | Float64       | 开盘价     |
| turnover       | Float64       | 成交额     |
| volume         | Float64       | 成交量     |
| low            | Float64       | 最低价     |


```python
  
```
     
###### tick数据(2笔/s)/all_tick

| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ----------|
| trading_date   | DateTime64(3) | 交易日     |
| datetime       | DateTime64(3) | 交易时间   |
| symbol         | String        | 交易品种   |
| contract       | String        | 合约名称   |
| open           | Float64       | 开盘价     |
| high           | Float64       | 最高价     |
| low            | Float64       | 最低价     |
| pre_close      | Float64       | 昨日收盘价 |
| open_interest  | Float64       | 持仓量     |
| pre_settlement | Float64       | 昨日结算价 |
| settlement     | Float64       | 结算价     |
| turnover       | Float64       | 成交额     |
| volume         | Float64       | 成交量     |
| up_limit       | Float64       | 涨停价     |
| down_limit     | Float64       | 跌停价     |
| last_price     | Float64       | 收盘价     |
| bid_price1 | Float64   | 买一价 |
| bid_vol1 | Float64   | 买一量 |
| ask_price1 | Float64   | 卖一价 |
| ask_vol1 | Float64   | 卖一量 |
| bid_price2 | Float64   | 买二价 |
| bid_vol2 | Float64   | 买二量 |
| ask_price2 | Float64   | 卖二价 |
| ask_vol2 | Float64   | 卖二量 |
| bid_price3 | Float64   | 买三价 |
| bid_vol3 | Float64   | 买三量 |
| ask_price3 | Float64   | 卖三价 |
| ask_vol3 | Float64   | 卖三量 |
| bid_price4 | Float64   | 买四价 |
| bid_vol4 | Float64   | 买四量 |
| ask_price4 | Float64   | 卖四价 |
| ask_vol4 | Float64   | 卖四量 |
| bid_price5 | Float64   | 买五价 |
| bid_vol5 | Float64   | 买五量 |
| ask_price5 | Float64   | 卖五价 |
| ask_vol5 | Float64   | 卖五量 |

```python
  
```
4. 委托信息/quote_data
    1. orderbook逐笔委托数据
    2. 具体到某个账户的订单数据

#### 交易数据/trade

##### 期货会员持仓数据/memeber_position_info

| 字段                        | 数据类型      | 含义         |
| --------------------------- | ------------- | ------------ |
| 字段                        | 数据类型      | 含义         |
| trading_date                | DateTime64(3) | 交易日       |
| contract                    | String        | 合约名称     |
| rank_type                   | String        | 排名方式     |
| rank_value                  | int64         | 排名序号     |
| member_name                 | String        | 会员名称     |
| member_open_interest        | String        | 会员持仓     |
| member_open_interest_change | Int64         | 会员持仓变化 |


```python
  
```

##### 大客户持仓数据

#### 指数数据/index

##### 大宗商品指数
##### blablabla ~


#### 另类数据/alternative


##### 交割库存数据

| 字段                            | 数据类型      | 含义       |
| ------------------------------- | ------------- | ---------- |
| trading_date                    | DateTime64(3) | 交易日     |
| symbol                          | String        | 交易品种   |
| warehouse_name                  | String        | 交割仓库名 |
| warehouse_receipt_number        | int64         | 库存       |
| unit                            | String        | 单位       |
| warehouse_receipt_number_change | Float64       | 库存变化   |

```python
  
```

1. 现货价格数据
2. 现货库存数据
3. 现货上下游数据

### 股票数据/stock

#### 主数据/master


##### 交易日信息/trading_date_info

| 字段         | 数据类型      | 含义   |
| :----------- | ------------- | ------ |
| trading_date | DateTime64(3) | 交易日 |


```python
  
```
###### 上市公司的基本信息/code_info
     
| 字段           | 数据类型      | 含义     |
| -------------- | ------------- | -------- |
| code           | String        | 证券代码 |
| trading_date   | DateTime64(3) | 交易日   |
| name           | String        | 证券名称 |
| exchange       | String        | 交易所   |
| listing_date   | String        | 上市日期 |
| delisting_date | String        | 退市日期 |


```python

```
   
3. 上市公司的分类信息
    1. 中信二级行业分类
    
4. 股票交易所的基本规则

#### 行情数据/md

##### 日行情数据/all_1d

| 字段         | 数据类型      | 含义       |
| ------------ | ------------- | ---------- |
| trading_date | DateTime64(3) | 交易日期   |
| code         | String        | 证券代码   |
| high         | Float64       | 最高价     |
| open         | Float64       | 开盘价     |
| low          | Float64       | 最低价     |
| close        | Float64       | 收盘价     |
| volume       | Float64       | 成交量     |
| turnover     | Float64       | 成交额     |
| trade_num    | Float64       | 交易笔数   |
| pre_close    | Float64       | 昨日收盘价 |
| up_limit     | Float64       | 涨停价     |
| down_limit   | Float64       | 涨停价     |


```python
  
```
##### 复权因子数据/adjust_factor

| 字段               | 数据类型      | 含义       |
| ------------------ | ------------- | ---------- |
| divid_operate_date | DateTime64(3) | 除权日     |
| code               | String        | 证券代码   |
| qfq_factor         | Float64       | 前复权因子 |
| hfq_factor         | Float64       | 后复权因子 |


```python
  
```
##### 切片行情数据/throttled_data
###### 30分钟数据/all_30m

| 字段         | 数据类型      | 含义       |
| ------------ | ------------- | ---------- |
| trading_date | DateTime64(3) | 交易日期   |
| code         | String        | 证券代码   |
| high         | Float64       | 最高价     |
| open         | Float64       | 开盘价     |
| low          | Float64       | 最低价     |
| close        | Float64       | 收盘价     |
| volume       | Float64       | 成交量     |
| turnover     | Float64       | 成交额     |
| trade_num    | Float64       | 交易笔数   |

```python
  
```
###### 5分钟数据/all_5m

| 字段         | 数据类型      | 含义       |
| ------------ | ------------- | ---------- |
| trading_date | DateTime64(3) | 交易日期   |
| code         | String        | 证券代码   |
| high         | Float64       | 最高价     |
| open         | Float64       | 开盘价     |
| low          | Float64       | 最低价     |
| close        | Float64       | 收盘价     |
| volume       | Float64       | 成交量     |
| turnover     | Float64       | 成交额     |
| trade_num    | Float64       | 交易笔数   |

```python
  
```
###### 1分钟数据/all_1m

| 字段         | 数据类型      | 含义       |
| ------------ | ------------- | ---------- |
| trading_date | DateTime64(3) | 交易日期   |
| code         | String        | 证券代码   |
| high         | Float64       | 最高价     |
| open         | Float64       | 开盘价     |
| low          | Float64       | 最低价     |
| close        | Float64       | 收盘价     |
| volume       | Float64       | 成交量     |
| turnover     | Float64       | 成交额     |
| trade_num    | Float64       | 交易笔数   |

```python
  
```
###### tick数据(2笔/s)/all_tick

| 字段           | 数据类型      | 含义       |
| -------------- | ------------- | ----------|
| trading_date   | DateTime64(3) | 交易日     |
| datetime       | DateTime64(3) | 交易时间   |
| code           | String        | 股票代码   |
| open           | Float64       | 开盘价     |
| high           | Float64       | 最高价     |
| low            | Float64       | 最低价     |
| pre_close      | Float64       | 昨日收盘价 |
| turnover       | Float64       | 成交额     |
| volume         | Float64       | 成交量     |
| up_limit       | Float64       | 涨停价     |
| down_limit     | Float64       | 跌停价     |
| last_price     | Float64       | 收盘价     |
| bid_price1 | Float64   | 买一价 |
| bid_vol1 | Float64   | 买一量 |
| ask_price1 | Float64   | 卖一价 |
| ask_vol1 | Float64   | 卖一量 |
| bid_price2 | Float64   | 买二价 |
| bid_vol2 | Float64   | 买二量 |
| ask_price2 | Float64   | 卖二价 |
| ask_vol2 | Float64   | 卖二量 |
| bid_price3 | Float64   | 买三价 |
| bid_vol3 | Float64   | 买三量 |
| ask_price3 | Float64   | 卖三价 |
| ask_vol3 | Float64   | 卖三量 |
| bid_price4 | Float64   | 买四价 |
| bid_vol4 | Float64   | 买四量 |
| ask_price4 | Float64   | 卖四价 |
| ask_vol4 | Float64   | 卖四量 |
| bid_price5 | Float64   | 买五价 |
| bid_vol5 | Float64   | 买五量 |
| ask_price5 | Float64   | 卖五价 |
| ask_vol5 | Float64   | 卖五量 |


```python
  
```

3. 委托信息/quote_data
    1. orderbook逐笔委托数据
    2. 具体到某个账户的订单数据

#### 交易数据/trade

1. 股票每日资金流入流出数据
2. 股票融资融券数据
3. 公募基金持仓数据
4. 私募基金持仓数据
5. 沪深港通每日额度数据
6. 北向资金持仓明细数据
7. 北向资金实时资金流向
8. 龙虎榜数据

#### 指数数据/index

##### 指数成分/index_component_info

| 字段         | 数据类型 | 含义     |
| ------------ | -------- | -------- |
| trading_date | String   | 交易日期 |
| code         | String   | 证券代码 |
| code_name    | String   | 证券名称 |
| index_code   | String   | 指数名称 |

```python
  
```

    2. 指数行情
    3. 升贴水数据
2. 中证500指数
    1. 成分股每日权重
    2. 指数价格
    3. 升贴水数据
3. 上证50指数
4. 行业指数

#### 另类数据/alternative

1. 上市公司财务信息
2. 上市公司公告/快报
3. 上市公司分红数据
4. 大宗交易信息
5. 十大流通股东信息
6. 十大股东信息
7. 热点/舆情信息
8. 电商数据
9. 新闻分析数据

### 基金数据/fund

#### 主数据/master

1. 各公募基金的基本信息
2. 基金风格/类型数据

#### 行情数据/md

1. 日数据/daily_data
    1. 每日净值数据
    2. 每日规模数据

#### 交易数据/trade

 1.基金持仓信息

#### 另类数据/alternative

1. 基金评级信息
2. 基金费率信息

### 期权数据/option

#### 主数据/master

1. 期权合约基本信息

#### 行情数据/md

1. 日行情数据/daily_data
2. 切片行情数据/throttled_data
    1. 30分钟数据/min30
    2. 5分钟数据/min5
    3. 1分钟数据/min1
    4. tick数据(2笔/s)
3. 委托信息/quote_data
    1. orderbook逐笔委托数据

### 债券数据/bond

- 银行间拆借利率

## 新加坡数据：

### 期货数据/future

#### 主数据/master

1. 商品期货的基本信息
2. 交易所的基本规则

#### 行情数据/md

1. 日行情数据/daily_data

#### 指数数据/index

1. 大宗商品指数
2. blablabla ~

## 国际数据：

### 加密货币数据

#### 主数据/master

1. 商品期货的基本信息
2. 交易所的基本规则

#### 行情数据/md

1. 日行情数据/daily_data
2. 切片行情数据/throttled_data
    1. 30分钟数据/min30
    2. 5分钟数据/min5
    3. 1分钟数据/min1
    4. tick数据(2笔/s)
3. 委托信息/quote_data
    1. orderbook逐笔委托数据
    2. 具体到某个账户的订单数据

### 宏观经济数据

### 外汇数据
