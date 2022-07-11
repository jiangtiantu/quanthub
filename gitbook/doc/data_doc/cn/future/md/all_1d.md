
 #  all_1d 
|    | name           | pandas_type   | numpy_type     | 释义       |
|---:|:---------------|:--------------|:---------------|:-----------|
|  0 | trading_date   | datetime      | datetime64[ns] | 交易日期   |
|  1 | contract       | unicode       | object         | 合约名称   |
|  2 | symbol         | unicode       | object         | 交易品种   |
|  3 | open           | float64       | float64        | 开盘价     |
|  4 | close          | float64       | float64        | 收盘价     |
|  5 | high           | float64       | float64        | 最高价     |
|  6 | low            | float64       | float64        | 最低价     |
|  7 | settlement     | float64       | float64        | 结算价     |
|  8 | pre_settlement | float64       | float64        | 昨日结算价 |
|  9 | up_limit       | float64       | float64        | 涨停价     |
| 10 | down_limit     | float64       | float64        | 跌停价     |
| 11 | open_interest  | float64       | float64        | 持仓量     |
| 12 | volume         | float64       | float64        | 成交量     |
| 13 | turnover       | float64       | float64        | 成交额     |
| 14 | pre_close      | float64       | float64        | 昨日收盘价 |
| 15 |                | int64         | int64          | nan        |
 ## 示例数据 
|       | trading_date   | contract   | symbol   |   open |   close |   high |   low |   settlement |   pre_settlement |   up_limit |   down_limit |   open_interest |   volume |    turnover |   pre_close |
|------:|:---------------|:-----------|:---------|-------:|--------:|-------:|------:|-------------:|-----------------:|-----------:|-------------:|----------------:|---------:|------------:|------------:|
| 22603 | 2022-06-01     | A2207      | A        |   6290 |    6278 |   6313 |  6255 |         6285 |             6291 |       6794 |         5788 |          103170 |    68484 | 4.30444e+09 |        6295 |
| 22774 | 2022-06-01     | A2209      | A        |   6275 |    6194 |   6285 |  6190 |         6242 |             6261 |       6761 |         5761 |           59405 |    24745 | 1.54476e+09 |        6270 |
| 22909 | 2022-06-01     | A2211      | A        |   6072 |    5999 |   6082 |  5995 |         6041 |             6075 |       6561 |         5589 |           29806 |    11666 | 7.04782e+08 |        6074 |
| 22999 | 2022-06-01     | A2301      | A        |   6043 |    5975 |   6048 |  5975 |         6012 |             6051 |       6535 |         5567 |            4867 |      509 | 3.06051e+07 |        6043 |
| 23054 | 2022-06-01     | A2303      | A        |   5981 |    5952 |   5990 |  5952 |         5969 |             6020 |       6501 |         5539 |             111 |       56 | 3.34276e+06 |        6020 |