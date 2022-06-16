# 命名规范

## ETL流程规则：

    1. download* 对应raw_data,只改trading_date(若有)这一个字段,其他不做任何数据上的调整。以文件的形式存储到本地磁盘;
    2. pretreat* 修改数据类型,字段重命名,添加新字段,存储到clickhouse
    3. process*  根据现在的数据表产生新的数据,比如指数数据,存储到clickhouse
    4. commercial* 对数据进行选择,是最终数据的集合,存储到clickhouse
    5. get:获取一个数据,放在内存中;
    6. save:从内存中,把处理过的数据,保存到本地;
    7. import: 指第一次把数据导入数据库;
    8. export: 把数据从数据库中导出为文件

## 命名大小写规则:
 
    1. 特定字段,symbol,method大写;
    2. 常量大写
    3. 数据源全为小写 
    4. 类,用大驼峰命名法,每个单词首字母大写;
    5. 其他函数或者变量,用下划线命名法,必须小写;
    6. comercial数据库,字段名全为小写


## 命名缩写规则：   

    1. 自己做的数据叫做diy,其他的数据源为缩写 
    2. sh 表示上海交易所,sz 表示深圳交易所 
    3. 数据字段尽量不要出现缩写
    4. 时间表达方式如下: 1y,1m,1d,1h,1m,1s
    5. 所有命名单词用下划线隔开,都是单数形式,尽量全拼,不要缩写
    6. 复杂变量名,用其数据类型作结尾,比如: trading_date_info_s

## 特殊命名规则：

    1. path 表示文件路径,dir表示文件夹路径;
    2. database代表mongo,clickhouse,mysql等等数据库;db代表具体的数据库名称
    3. tb:table db: database dt: date dtt: datetime rt：realtime his：history cal:calculate hs300:hs300指数 
    4. code,如510300,trade_code:如510300.sh 
    5. 所有字段名字统一,具有特定的意思,比如symbol /contract,默认所有的contract为symbol+4位数字；code/trade_code

## 数据存储类型规则：

    1. trading_date和datetime 数据类型都是datetime64
    2. 在把数据写到raw_data 里面时,原有的date,day 等表示日期的字段不动,数据类型也不动。自行添加trading_date字段
    3. 默认所有从数据库取出的所有数据都是DataFrame,不做sort操作


# 代码规范

    1. 代码用black格式化
    2. 代码模块化,少造轮子
    3. 注释用 :param
    4. 字符串拼接用f"{xxx}"
    5. 函数尽量写成传参数的方式

    

    