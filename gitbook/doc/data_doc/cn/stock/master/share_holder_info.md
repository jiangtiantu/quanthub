
 #  share_holder_info 
|    | name               | pandas_type   | numpy_type     | 释义                                                         |
|---:|:-------------------|:--------------|:---------------|:-------------------------------------------------------------|
|  0 | code               | unicode       | object         | 证券代码                                                     |
|  1 | info_date          | datetime      | datetime64[ns] | 公告日期                                                     |
|  2 | end_date           | datetime      | datetime64[ns] | 结束日期                                                     |
|  3 | rank               | int64         | int64          | 排名                                                         |
|  4 | shareholder_name   | unicode       | object         | 股东名称                                                     |
|  5 | shareholder_attr   | unicode       | object         | 股东属性                                                     |
|  6 | shareholder_kind   | unicode       | object         | 股东性质                                                     |
|  7 | shareholder_type   | empty         | object         | 股东类别                                                     |
|  8 | hold_percent_total | float64       | float64        | 占股比例(%)当fields='total'时，持股数(股)/总股本*100         |
|  9 | hold_percent_float | float64       | float64        | 占流通A股比例(%),无限售流通A股/已上市流通A股(不含高管股)*100 |
| 10 | share_pledge       | float64       | float64        | 股权质押涉及股数(股)                                         |
| 11 | share_freeze       | float64       | float64        | 股权冻结涉及股数(股)                                         |
| 12 |                    | int64         | int64          | nan                                                          |
 ## 示例数据 
|         |   code | info_date   | end_date   |   rank | shareholder_name                                                | shareholder_attr   | shareholder_kind   | shareholder_type   |   hold_percent_total |   hold_percent_float |   share_pledge |   share_freeze |
|--------:|-------:|:------------|:-----------|-------:|:----------------------------------------------------------------|:-------------------|:-------------------|:-------------------|---------------------:|---------------------:|---------------:|---------------:|
| 1538811 | 605090 | 2022-06-01  | 2022-05-24 |      1 | 中国农业银行股份有限公司-中邮核心优势灵活配置混合型证券投资基金 | 证券品种           | 开放式投资基金     | None               |             0.497732 |             2.65735  |            nan |            nan |
| 1538812 | 605090 | 2022-06-01  | 2022-05-24 |      2 | 中国工商银行股份有限公司-汇添富碳中和主题混合型证券投资基金     | 证券品种           | 开放式投资基金     | None               |             0.141364 |             0.754732 |            nan |            nan |
| 1538813 | 605090 | 2022-06-01  | 2022-05-24 |      3 | 张林                                                            | 自然人             | 自然人             | None               |             0.129219 |             0.689889 |            nan |            nan |
| 1538814 | 605090 | 2022-06-01  | 2022-05-24 |      4 | 中国建设银行股份有限公司-华夏盛世精选混合型证券投资基金         | 证券品种           | 开放式投资基金     | None               |             0.112874 |             0.602628 |            nan |            nan |
| 1538815 | 605090 | 2022-06-01  | 2022-05-24 |      5 | 顾电阳                                                          | 自然人             | 自然人             | None               |             0.102656 |             0.548072 |            nan |            nan |