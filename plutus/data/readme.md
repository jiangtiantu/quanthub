# data 模块分为：

该模块，仅向熟悉的QD或者代码贡献者全部开源，如有需要请私下联系。对于大部分人来说，不需要搞清楚数据的ETL，直接下载研究数据使用即可。

**研究数据下载地址：**

链接: https://pan.baidu.com/s/1nCZIXFtG7Hoe7OvXs1uknA?pwd=n2ru 提取码: n2ru 

数据存储格式为parquet，使用方式请查看pyarrow 或者 researchub 中的案例。

**实时交易数据：**

如有需求，请小窗联系，email:qiwu12@qq.com
**数据ETL简介:**

- data_download：原始数据的获取。同一份数据可以有多个数据源。
- data_pretreat：对原始数据进行预处理，进行数据格式，数据字段的统一
- data_process：对pretreat数据再进一步的处理，衍生新数据，比如zhu'li
- data_sync：数据的异地同步
- data_backup：数据的备份
- data_update：数据每日增量更新
- data_wrangle：数据的整理工具，包含数据重塑，去极值，标准化等等