
 #  allotment_info 
|    | name                          | pandas_type   | numpy_type     | 释义             |
|---:|:------------------------------|:--------------|:---------------|:-----------------|
|  0 | code                          | unicode       | object         | 证券代码         |
|  1 | declaration_announcement_date | datetime      | datetime64[ns] | 首次信息发布日期 |
|  2 | proportion                    | float64       | float64        | 计划配股比例     |
|  3 | allotted_proportion           | empty         | object         | 实际配股比例     |
|  4 | allotted_shares               | empty         | object         | 实际配股数量(股) |
|  5 | allotment_price               | empty         | object         | 每股配股价格(元) |
|  6 | book_closure_date             | empty         | object         | 股权登记日       |
|  7 | ex_right_date                 | empty         | object         | 除权除息日       |
 ## 示例数据 
|    |   code | declaration_announcement_date   |   proportion | allotted_proportion   | allotted_shares   | allotment_price   | book_closure_date   | ex_right_date   |
|---:|-------:|:--------------------------------|-------------:|:----------------------|:------------------|:------------------|:--------------------|:----------------|
|  0 | 600081 | 2022-06-29                      |          0.3 | None                  | None              | None              | None                | None            |