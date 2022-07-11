
 #  contract_info 
|    | name               | pandas_type   | numpy_type     | 释义         |
|---:|:-------------------|:--------------|:---------------|:-------------|
|  0 | contract           | unicode       | object         | 合约名称     |
|  1 | symbol             | unicode       | object         | 交易品种     |
|  2 | exchange           | unicode       | object         | 交易所代码   |
|  3 | multiplier         | float64       | float64        | 合约乘数     |
|  4 | listing_date       | datetime      | datetime64[ns] | 上市日期     |
|  5 | delisting_date     | datetime      | datetime64[ns] | 退市日期     |
|  6 | last_tradable_date | datetime      | datetime64[ns] | 最后可交易日 |
|  7 |                    | int64         | int64          | nan          |
 ## 示例数据 
|    | contract   | symbol   | exchange   |   multiplier | listing_date   | delisting_date   | last_tradable_date   |
|---:|:-----------|:---------|:-----------|-------------:|:---------------|:-----------------|:---------------------|
|  0 | A0303      | A        | DCE        |           10 | 2002-03-15     | 2003-03-14       | 2003-02-27           |
|  1 | A0305      | A        | DCE        |           10 | 2002-03-15     | 2003-05-23       | 2003-04-29           |
|  2 | A0307      | A        | DCE        |           10 | 2002-03-15     | 2003-07-14       | 2003-06-27           |
|  3 | A0309      | A        | DCE        |           10 | 2002-05-22     | 2003-09-12       | 2003-08-28           |
|  4 | A0311      | A        | DCE        |           10 | 2002-05-22     | 2003-11-14       | 2003-10-30           |