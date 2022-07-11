
 #  margin_info 
|    | name                     | pandas_type   | numpy_type     | 释义         |
|---:|:-------------------------|:--------------|:---------------|:-------------|
|  0 | code                     | unicode       | object         | 证券代码     |
|  1 | trading_date             | datetime      | datetime64[ns] | 交易日期     |
|  2 | margin_balance           | int64         | int64          | 融资余额     |
|  3 | buy_on_margin_value      | int64         | int64          | 融资买入额   |
|  4 | short_sell_quantity      | int64         | int64          | 融券余量     |
|  5 | margin_repayment         | float64       | float64        | 融资偿还额   |
|  6 | short_balance_quantity   | int64         | int64          | 融券余量     |
|  7 | short_repayment_quantity | float64       | float64        | 融券偿还量   |
|  8 | short_balance            | float64       | float64        | 融券余额     |
|  9 | total_balance            | float64       | float64        | 融资融券余额 |
| 10 |                          | int64         | int64          | nan          |
 ## 示例数据 
|       |   code | trading_date   |   margin_balance |   buy_on_margin_value |   short_sell_quantity |   margin_repayment |   short_balance_quantity |   short_repayment_quantity |    short_balance |   total_balance |
|------:|-------:|:---------------|-----------------:|----------------------:|----------------------:|-------------------:|-------------------------:|---------------------------:|-----------------:|----------------:|
|  2956 | 000001 | 2022-06-01     |       3946277760 |             125686147 |                393600 |        9.33743e+07 |                 14830709 |           182600           |      2.08816e+08 |     4.15509e+09 |
|  5914 | 000002 | 2022-06-01     |       4692882274 |             105554343 |                458800 |        1.13556e+08 |                  9536402 |           602203           |      1.70511e+08 |     4.86339e+09 |
|  8182 | 000006 | 2022-06-01     |        399300756 |              40245137 |                 39400 |        3.87926e+07 |                   116600 |            35100           | 529364           |     3.9983e+08  |
|  9066 | 000008 | 2022-06-01     |        275824636 |              65369028 |                     0 |        7.84355e+07 |                   192000 |              300           | 512640           |     2.76337e+08 |
| 11616 | 000009 | 2022-06-01     |       1940339971 |             303701902 |               1117014 |        1.0957e+08  |                  4635980 |                1.55181e+06 |      5.79498e+07 |     1.99829e+09 |