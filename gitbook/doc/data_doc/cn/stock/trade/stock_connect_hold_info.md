
 #  stock_connect_hold_info 
|      | name                   | pandas_type | numpy_type     | 释义           |
| ---: | :--------------------- | :---------- | :------------- | :------------- |
|    0 | code                   | unicode     | object         | 证券代码       |
|    1 | trading_date           | datetime    | datetime64[ns] | 交易日期       |
|    2 | shares_holding         | float64     | float64        | 持股量         |
|    3 | holding_ratio          | float64     | float64        | 持股比例       |
|    4 | adjusted_holding_ratio | float64     | float64        | 调整后持股比例 |
|    5 |                        | int64       | int64          | nan            |
 ## 示例数据 
|      |   code | trading_date | shares_holding | holding_ratio | adjusted_holding_ratio |
| ---: | -----: | :----------- | -------------: | ------------: | ---------------------: |
| 1637 | 000001 | 2022-06-01   |    1.70297e+09 |          8.77 |                 8.7757 |
| 3294 | 000002 | 2022-06-01   |    4.16618e+08 |          4.28 |                 4.2873 |
| 4951 | 000005 | 2022-06-01   |           2010 |             0 |                 0.0002 |
| 6608 | 000006 | 2022-06-01   |    4.74077e+06 |          0.35 |                 0.3512 |
| 8240 | 000008 | 2022-06-01   |    4.07149e+07 |          1.46 |                 1.5114 |