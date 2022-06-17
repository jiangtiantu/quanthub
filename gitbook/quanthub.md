# quanthub简介

<p>
<p align="center">
    <img src="https://s1.328888.xyz/2022/06/17/0LGiy.png">
</p>

<p align="center">
        <img src="https://img.shields.io/static/v1?style=flat-square&message=centos&color=E95420&logo=centos&logoColor=FFFFFF&label=">
    <a href="https://github.com/jiangtiantu/quanthub/issues">
        <img src="https://img.shields.io/github/issues/jiangtiantu/quanthub?style=flat-square&color=blue">
    </a>
    <a href="https://github.com/jiangtiantu/quanthub/pulls">
        <img src="https://img.shields.io/github/issues-pr/jiangtiantu/quanthub?style=flat-square&color=brightgreen" alt=",">
    </a>
    <a href="https://github.com/jiangtiantu/quanthub/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/jiangtiantu/quanthub?&style=flat-square">
    </a>
</p>

<p align="center">
    <a href="https://github.com/jiangtiantu/quanthub/issues">报告问题</a>
    ·
    <a href="https://github.com/jiangtiantu/quanthub/issues">功能需求</a>
</p>

<p align="center">一个轻量清晰,容易上手的,数据/投研/交易集成框架</p>

## 🐼**QuantHub简介(持续更新调整中ing)**

首先 QuantHub 是个圈地自萌的小社区,里面的人个个是人才,长得好看(❤´艸｀❤),说话又好听。

其次 quanthub 是个体验感很好的量化集成框架,目前开源的是实际生产环境的一个简化版本,几乎涵盖了（数据/投研/组合/交易/分析）所有环节。

它足够简单,足够自由,你可以像搭积木一样,搭配自己喜欢的技术栈,让它成为最适合你的开发利器！

它的架构肯定是没有问题的,几乎可以说是很标准了,搭配合适的技术栈,是可以成为一个企业级的框架的；

最后,感谢这两年多来,不断支持 QuantHub项目成长,给予帮助和建议的朋友🍑🍑🍑~

- 项目地址： https://gitee.com/jiangtiantu/quanthub
- 文档地址： http://jiangtiantu.gitee.io/quanthub

## ✨ 工具特性

- 自由,自由,还是\*\*\*D 自由,你可以随心所欲的魔改 DIY,可扩展,可升级；

- 简单,简单,足够轻松上手的简单,这是一整套完整的体系,来源于实际的各生产环节；

## 💻 项目结构

quanthub包含以下几个部分（请原谅我是个取名废材,o(*////▽////*)q）：

### **datahub**
  - 这是一个落地数据库,你可以直接把你想要的数据放到本地,并通过data_sync进行每日同步更新。
  - 储存形式任意,你可以按照自己的喜好进行选择,目前我实际生产环境用的clickhouse+parquet+duckdb；
  - 该数据库包含：股票,期货,期权,基金的历史行情数据,以及相应的实时数据；
  - 数据的ETL相关代码,请查阅plutus.data 模块 
  - 该数据库还包含,各种另类数据和基本面数据,具体内容,请查看datahub 文档；

### **factorhub**
  - 这是落地一个因子数据库,可以是你喜欢的任意形式,为方便上传,该项目采用的parquet文件存储；
- 也是一个因子回测框架,包含截面因子回测和时序因子回测两大类；
  - 投研环境下,相关回测逻辑,请阅读plutus.research模块
  - 生产环境下,批量计算因子,请查看plutus.factor模块
- 因子面板(更新中); 
- 一个因子交换和交流平台(目前是以微信群的方式),有想加入的小伙伴,请私下联系；
- 具体内容说明,请查看factorhub文档；

### **signalhub**
- 这是落地一个信号数据库,是对因子数据的进一步处理,可以是你喜欢的任意形式,为方便上传,该项目采用的parquet文件存储；
- 生产环境下,批量计算信号,请查看plutus.signal 模块
- 交易信号面板(更新中);
- 大部分人可能用不到这个模块,如果不需要篮子交易的话；
- 具体内容说明,请查看signalhub文档；

### **positionhub**
  - 这是落地一个账户持仓数据库,是对信号数据的进一步处理,可以是你喜欢的任意形式；
- 生产环境下,批量计算信号,请查看plutus.position模块
- 大部分人可能用不到这个模块,如果不需要篮子交易,或者需要多账户交易的话；
- 具体内容说明,请查看positionhub文档；

### **researhub**
  - 投研平台,本质是jupyter lab；
  - 我对该模块的定义是存放,我们数据分析的各类notebook文件,以及各种测试代码；
  - 具体内容说明,请查看researhub文档；
### **paperhub**
  - 一个放资料的地方,包含各类视频和各种PDF等等文件,几乎你能在互联网上找到的所有可能有点用的学习资料
  - 资料总大小大概200g 左右,分类如下：
    - 股票
    - 基金
    - 期货
    - 期权
    - 资产配置
    - 高频
    - 债券
  - 具体内容说明,请查看paperhub文档；

### **tradehub**
- 关于交易,我们的理念是,不同标的,不同策略,可能需要的交易框架是不一样的。你喜欢的,适合的就是最好的；
- 所以,我们直接集成了一些优秀的开源交易框架：
  - wondertrader
  - ctpbee
  - fk_ctp
  - 期待能与更多的开源框架作者建立联系,感谢你们为开源社区做出的贡献~
- 具体内容说明,请查看tradehub文档；
### **jobhub**
  - 一个方便同行进行招聘与求职的板块
  - 目前是和以下金融ip小伙伴,同步更新,微信公众号,知乎等等自媒体；
    - FOF小菜鸟；
    - 期待能与更多的金融自媒体和IP建立联系
  - 具体内容说明,请查看jobhub文档；

### **gamehub**
  - 一个业内朋友一起打游戏的板块；
  - 具体内容说明,请查看gamehub文档；

### **lovehub**
  - 一个征婚交友的地方；
  - 具体内容说明,请查看lovehub文档；

### plutus（核心）
  - plutus是另外一个小伙伴给起的名字，翻译为财神爷，哈哈，是不是凭这个就该关注下了呢
  - 后台框架,该项目核心,分为以下模块和文件:


```bash
├─data
│  │  data_base.py
│  │  __init__.py
│  │
│  ├─data_backup
│  │      backup_data.py
│  │      __init__.py
│  │
│  ├─data_download
│  │      download_base.py
│  │      download_from_bs.py
│  │      download_from_ctp.py
│  │      download_from_sge.py
│  │      __init__.py
│  │
│  ├─data_prepare
│  │      prepare_base.py
│  │      prepare_center_data.py
│  │      prepare_his_parquet.py
│  │      prepare_rt_redis.py
│  │      __init__.py
│  │
│  ├─data_pretreat
│  │      pretreat_base.py
│  │      pretreat_from_bs.py
│  │      pretreat_from_diy.py
│  │      __init__.py
│  │
│  ├─data_process
│  │      process_base.py
│  │      process_cn_future_index.py
│  │      process_cn_future_md.py
│  │      process_cn_future_master.py
│  │      process_cn_future_trade.py
│  │      process_cn_stock_master.py
│  │      process_cn_stock_trade.py
│  │      process_sg_future_md.py
│  │      __init__.py
│  │
│  ├─data_sync
│  │      __init__.py
│  │      sync_base.py
│  │      sync_data.py
│  │
│  ├─data_update
│  │      update_base.py
│  │      update_data.py
│  │      __init__.py
│  │
│  └─data_wrangle
│          resample_data.py
│          standard_data.py
│          __init__.py
│
├─execution
│      cal_factor.bat
│      cal_signal.bat
│      run_prepare_data.bat
│      run_update_data.bat
│
├─factor
│  │  factor_base.py
│  │  __init__.py
│  │
│  ├─factor_calculate
│  │      cal_cn_future_cs_1d.py
│  │      cal_cn_future_ts_1d.py
│  │      cal_factor_base.py
│  │      __init__.py
│  │
│  ├─factor_define
│  │      cn_future_cs_1d_mom.py
│  │      cn_future_ts_1d_mom.py
│  │      __init__.py
│  │
│  ├─factor_operator
│  │      cs_operator.py
│  │      ts_operator.py
│  │      __init__.py
│  │
│  └─factor_process
│          __init__.py
│
├─position
│  │  position_base.py
│  │  __init__.py
│  │
│  ├─position_calculate
│  │      cal_cn_future_cs_1d.py
│  │      cal_position_base.py
│  │      __init__.py
│  │
│  └─position_process
│          process_position.py
│          __init__.py
│
├─research
│  │  __init__.py
│  │
│  ├─backtest
│  │  │  backtest.py
│  │  │  statistics.py
│  │  │  __init__.py
│  │
│  ├─models
│  │      predict_model.py
│  │      train_model.py
│  │      __init__.py
│
├─signal
│  │  signal_base.py
│  │  __init__.py
│  │
│  ├─signal_calculate
│  │      cal_cn_future_cs_1d.py
│  │      cal_signal_base.py
│  │      __init__.py
│  │
│  ├─signal_portfolio
│  │      cal_portfolio_weight.py
│  │      __init__.py
│  │
│  └─signal_process
│          process_signal.py
│          __init__.py
│
├─trader
│      __init__.py
│
├─utils
│  │  __init__.py
│  │
│  ├─database
│  │      ck_control.py
│  │      dk_control.py
│  │      __init__.py
│  │
│  ├─exception
│  │      error.py
│  │      __init__.py
│  │
│  ├─tool
│  │      add_sys_path.py
│  │      configer.py
│  │      datetime_wrangle.py
│  │      decorator.py
│  │      email.py
│  │      freeze_requirement.py
│  │      logger.py
│  │      requirements.txt
│  │      __init__.py
│  │
│  ├─visualization
│  │  │  plot.py
```

## 🚀 使用说明

### 第一步：克隆仓库

确保服务器安装了 Git,否则需要先 安装 git 命令安装软件：

```bash
git clone https://github.com/jiangtiantu/quanthub.git
```

如果因为网络问题无法连接,可以使用国内镜像仓库,但是镜像仓库会有 `30` 分钟的延迟：

```bash
git clone https://gitee.com/jiangtiantu/quanthub.git
```

或者直接点击项目右上角下载；

### 第二步：构建你的想法

根据你的经验,你的猜测,提出一个可能的投研思路,一个研究和交易的方向。 如果你没有任何想法,可以先看看paperhub中的资料,找找灵感

### 第三步：获取数据

- 查看datahub面板数据,根据你的思路,选取你需要的数据。

### 第四步：打开投研DEMO,享受你的量化之旅

- 在researhub里有为你准备好的大量投研demo,请查看reasearhub

### 第五步：将数据转化为因子

- 正常情况下,先做单因子分析
- 如果已经有很成熟的因子库了,走factor,signal 批量生成和转化,将数据存放到factorhub,signalhub

### 第六步：将因子转化为实际交易的仓位

- 这里会涉及到因子组合和信号组合两个问题,确定自己需要怎样的组合方式,将结果输出到positionhub

### 第七步：选择喜欢的合适的交易框架

- 看看tradehub 中有没有你喜欢的交易框架,尽量少造轮子呀
- 当然,非常欢迎大佬提交自己的框架,多多宜善

### 第八步：评估分析,优化提高

- 一个循环...

## 📝 升级打怪之路

```bash
ok,走过了上面的流程,你已经掌握了量化投资的基本套路了。
接下来,或自己,或和小伙伴,开启新的升级打怪之路了!!!!
这个行业真的是太jer卷了,例如期货市场,本质上就是一个零和博弈的市场。
在这个赌场里,如果你不能跟随市场成长和进化,那么你就是那只被抓的🐟🐋🐳🐬；
如果你不知道怎么避免成为一个韭菜,那么你就是那个韭菜！
所以,做好一直卷下去的准备吧；
如果你准备好了,那就去尝试吧,每次失败的经验,都将帮助你逼近那些正确的方向！

但一定一定,切记,投资有风险,入市需谨慎；活下来,比什么都重要！
# 生活不易,猫猫叹气,加油(ง •_•)ง！
```

## 🤝 参与共建
- 要做的东西太多了,本项目应该会处于长期快速迭代更新；
- 我们欢迎所有的贡献者,也期待能结识更多金融圈开源小伙伴,你可以将任何想法作为 pull requests 或 GitHub issues 提交。关于代码如果有任何疑惑的地方,可以先看下,name_rule是否能解决问题。顺颂商祺 :)
