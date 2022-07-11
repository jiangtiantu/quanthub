
 #  symbol_info 
|    | name               | pandas_type   | numpy_type   | 释义                            |
|---:|:-------------------|:--------------|:-------------|:--------------------------------|
|  0 | symbol             | unicode       | object       | 交易品种                        |
|  1 | price_tick         | float64       | float64      | 最小价格变动单位                |
|  2 | multiplier         | float64       | float64      | 合约乘数                        |
|  3 | exchange_tq        | unicode       | object       | 交易所合约代码(天勤)            |
|  4 | exchange_wind      | unicode       | object       | 交易所合约代码(wind)            |
|  5 | index_code_wind    | unicode       | object       | nan                             |
|  6 | dominant_code_wind | unicode       | object       | nan                             |
|  7 | exchange_ctp       | unicode       | object       | 交易所合约代码(ctp)             |
|  8 | day_before_expiry  | int64         | int64        | 到期日-普通交易者最后可持有日期 |
 ## 示例数据 
|    | symbol   |   price_tick |   multiplier | exchange_tq   | exchange_wind   | index_code_wind   | dominant_code_wind   | exchange_ctp   |   day_before_expiry |
|---:|:---------|-------------:|-------------:|:--------------|:----------------|:------------------|:---------------------|:---------------|--------------------:|
|  0 | A        |         1    |           10 | DCE           | DCE             | AFI.WI            | A.DCE                | DCE            |                  21 |
|  1 | AG       |         1    |           15 | SHFE          | SHF             | AGFI.WI           | AG.SHF               | SHFE           |                  15 |
|  2 | AL       |         5    |            5 | SHFE          | SHF             | ALFI.WI           | AL.SHF               | SHFE           |                  15 |
|  3 | AP       |         1    |           10 | CZCE          | CZC             | APLFI.WI          | AP.CZC               | CZCE           |                  21 |
|  4 | AU       |         0.02 |         1000 | SHFE          | SHF             | AUFI.WI           | AU.SHF               | SHFE           |                  15 |