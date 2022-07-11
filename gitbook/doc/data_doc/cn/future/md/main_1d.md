
 #  main_1d 
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
|       | trading_date   | contract   | symbol   |    open |    close |     high |      low |   settlement |   pre_settlement |   up_limit |   down_limit |   open_interest |   volume |    turnover |   pre_close |
|------:|:---------------|:-----------|:---------|--------:|---------:|---------:|---------:|-------------:|-----------------:|-----------:|-------------:|----------------:|---------:|------------:|------------:|
| 62236 | 2022-06-01     | A2207      | A        |  6290   |  6278    |  6313    |  6255    |      6285    |           6291   |     6794   |      5788    |          103170 |    68484 | 4.30444e+09 |     6295    |
| 62237 | 2022-06-01     | AG2212     | AG       |  4695   |  4673    |  4727    |  4657    |      4689    |           4722   |     5194   |      4249    |          440890 |   336900 | 2.37006e+10 |     4716    |
| 62238 | 2022-06-01     | AL2207     | AL       | 20650   | 20280    | 20695    | 20030    |     20320    |          20775   |    22850   |     18695    |          186703 |   378926 | 3.84989e+10 |    20795    |
| 62239 | 2022-06-01     | AP2210     | AP       |  8816   |  8806    |  8945    |  8792    |      8876    |           8818   |     9612   |      8024    |          149846 |   183907 | 1.63236e+10 |     8853    |
| 62240 | 2022-06-01     | AU2212     | AU       |   399.6 |   397.46 |   400.68 |   396.76 |       398.34 |            400.2 |      432.2 |       368.18 |           93080 |    39983 | 1.59271e+10 |      400.26 |