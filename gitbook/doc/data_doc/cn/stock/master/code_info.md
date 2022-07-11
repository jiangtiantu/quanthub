
 #  code_info 
|    | name           | pandas_type   | numpy_type     | 释义                                                                  |
|---:|:---------------|:--------------|:---------------|:----------------------------------------------------------------------|
|  0 | trading_date   | datetime      | datetime64[ns] | 交易日期                                                              |
|  1 | code           | unicode       | object         | 证券代码                                                              |
|  2 | name           | unicode       | object         | 名称                                                                  |
|  3 | issue_price    | float64       | float64        | 发行价                                                                |
|  4 | board_type     | unicode       | object         | 板块类别，'MainBoard'-主板,'GEM'-创业板,'SME'-中小企业板,'KSH'-科创板 |
|  5 | listing_date   | unicode       | object         | 上市日期                                                              |
|  6 | delisting_date | unicode       | object         | 退市日期                                                              |
|  7 |                | int64         | int64          | nan                                                                   |
 ## 示例数据 
|         | trading_date   |   code | name     |   issue_price | board_type   | listing_date   | delisting_date   |
|--------:|:---------------|-------:|:---------|--------------:|:-------------|:---------------|:-----------------|
| 9167596 | 2022-06-01     | 000001 | 平安银行 |            40 | MainBoard    | 1991-04-03     | 0000-00-00       |
| 9167597 | 2022-06-01     | 000002 | 万科A    |             1 | MainBoard    | 1991-01-29     | 0000-00-00       |
| 9167598 | 2022-06-01     | 000004 | ST国华   |             1 | MainBoard    | 1990-12-01     | 0000-00-00       |
| 9167599 | 2022-06-01     | 000005 | ST星源   |            10 | MainBoard    | 1990-12-10     | 0000-00-00       |
| 9167600 | 2022-06-01     | 000006 | 深振业A  |            10 | MainBoard    | 1992-04-27     | 0000-00-00       |