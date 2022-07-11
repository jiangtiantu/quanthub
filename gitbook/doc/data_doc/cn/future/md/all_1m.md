
 #  all_1m 
|    | name          | pandas_type   | numpy_type     | 释义     |
|---:|:--------------|:--------------|:---------------|:---------|
|  0 | trading_date  | datetime      | datetime64[ns] | 交易日期 |
|  1 | trading_time  | datetime      | datetime64[ns] | 交易时间 |
|  2 | contract      | unicode       | object         | 合约名称 |
|  3 | symbol        | unicode       | object         | 交易品种 |
|  4 | open          | float64       | float64        | 开盘价   |
|  5 | close         | float64       | float64        | 收盘价   |
|  6 | high          | float64       | float64        | 最高价   |
|  7 | low           | float64       | float64        | 最低价   |
|  8 | open_interest | float64       | float64        | 持仓量   |
|  9 | volume        | float64       | float64        | 成交量   |
| 10 | turnover      | float64       | float64        | 成交额   |
| 11 |               | int64         | int64          | nan      |
 ## 示例数据 
|       | trading_date        | trading_time        | contract   | symbol   |   open |   close |   high |   low |   open_interest |   volume |   turnover |
|------:|:--------------------|:--------------------|:-----------|:---------|-------:|--------:|-------:|------:|----------------:|---------:|-----------:|
| 39540 | 2022-06-01 00:00:00 | 2022-05-31 21:01:00 | FU2302     | FU       |   4054 |    4054 |   4054 |  4054 |           16708 |      650 | 2.6351e+07 |
| 39541 | 2022-06-01 00:00:00 | 2022-05-31 21:02:00 | FU2302     | FU       |   4054 |    4054 |   4054 |  4054 |           16708 |        0 | 0          |
| 39542 | 2022-06-01 00:00:00 | 2022-05-31 21:03:00 | FU2302     | FU       |   4054 |    4054 |   4054 |  4054 |           16708 |        0 | 0          |
| 39543 | 2022-06-01 00:00:00 | 2022-05-31 21:04:00 | FU2302     | FU       |   4054 |    4054 |   4054 |  4054 |           16708 |        0 | 0          |
| 39544 | 2022-06-01 00:00:00 | 2022-05-31 21:05:00 | FU2302     | FU       |   4054 |    4054 |   4054 |  4054 |           16708 |        0 | 0          |