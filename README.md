# AUTO-EARN
[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/)

![image-20200521115729378](pic/README/image-20200521115729378.png)

## 目录结构

```
│  app.py  //前台展示
│  autoearn.py  //程序入口
│  README.md
│  requirements.txt  
│  server.py  //漏洞推送、通知提醒
│  start.sh  //启动相关程序、日志记录
│  stop.sh
│  subdomain_monitor.py  //子域收集监控、数据库保存
│  target.txt  //目标文件
│  
├─lib //插件目录
│      check_cdn.py  //cdn检查模块
│      config.py  //配置模块
│      craw_to_xray.py  //爬虫、漏洞抓取模块
│      port_check.py  //端口检测模块
│      read_target.py  //目标读取模块
│      run_html.py  //前台启动模块
│      server_push.py  //消息通知模块
│      sql_connect.py  //数据库相关模块
│      subdomain_collect.py  //子域收集模块
│      waf_check.py  //waf检测模块
│      __init__.py
│      
├─logs
│      crawlergo.log  //crawlergo日志
│      oneforall.log  //oneforall日志
│      server.log  //漏洞推送日志
│      subdomain_monitor.log //子域收集监控日志
│      xray.log
│      
├─pic
│  └─README
│          
├─results
│      result.sqlite3  //数据库
│      
├─templates
│      index.html //主页文件
│      
└─tools
    ├  crawlergo  //一个使用chrome headless模式进行URL入口收集的动态爬虫
    ├  chrome  //chrome浏览器
    ├  masscan //异步传输，无状态的扫描端口工具             
    ├  OneForAll  //一款功能强大的子域收集工具                      
    ├  wafcheck  //WAF指纹识别工具             
    └  xray  //一款躺着收洞的神器
```



## 工具流程

`AUTO-EARN`是一个利用[OneForAll](https://github.com/shmilylty/OneForAll)进行子域收集、[Shodan API](https://www.shodan.io/?language=en)端口扫描、[Wafw00f](https://github.com/EnableSecurity/wafw00f)进行WAF指纹识别、[Xray](https://xray.cool/xray/)漏洞Fuzz、[Server酱](http://sc.ftqq.com/3.version)的自动化漏洞扫描、由`Flask`支撑一个简单可视化界面，即时通知提醒的漏洞挖掘辅助工具，本质上更像是一个流程框架，完成各工具之前的自动化联动过程，这个工具执行流程如下

![image-20200521113836222](pic/README/image-20200521113836222.png)

首先通过`target.txt`读取到`目标`之后，由`OneForAll`后台进行子域名收集过程，然后通过`subdomain_monitor.py`进行监控，监测子域收集过程是否完成，完成后会通过`server酱`进行消息推送，并且存入本地数据库中的`SUBDOMAIN`表

![image-20200521142924673](pic/README/image-20200521142924673.png)

![image-20200521143631791](pic/README/image-20200521143631791.png)

在收集子域完成后，通过`端口检测`进行端口检测，目的是发现那些开放在其它端口上的`web`系统，从而能更全面的进行后续的检测，在端口检测过程中会首先通过`check_cdn.py`进行`CDN检测`，之后不存在`CDN`的目标再利用`shodan api`进行`端口检测`以及`服务识别`的过程，然后将检测到的目标按照`协议:DOMAIN:端口`的格式存储到`TASK`表中，如果目标存在`CDN`则默认返回`80`端口存储到`TASK`表中

![image-20200521143650507](pic/README/image-20200521143650507.png)

之后`WAF检测`过程会对`TASK`中的每个目标通过`Wafw00f`进行指纹识别，并且修改`TASK`表中的`WAF`字段，这里大家可以根据自己的需求再进行更改，比如舍弃存在`WAF`的目标

![image-20200521172538644](pic/README/image-20200521172538644.png)

`Fuzz`阶段会首先调用[crawlergo](https://github.com/0Kee-Team/crawlergo)使用`chrome headless`模式进行URL入口收集，我们可以利用`--push-to-proxy`来连接我们的被动扫描器[xray](https://github.com/chaitin/xray)进行漏洞扫描， `xray` 有一种漏洞输出模式叫 `webhook-output`，在发现漏洞的时候，将会向指定的 `url`以 `post`的方式传输漏洞数据，之后我们通过搭建一个 `web` 服务器，接收到 `xray` 发送的漏洞信息，然后在将它转发，我们借助于 `Python` 的 `flask` 框架构造了`server.py`，接下来就是解析 `xray` 的漏洞信息，然后生成对应的页面模板，之后通过`server酱`我们就可以将漏洞信息推送到我们的微信中

![image-20200521152101746](pic/README/image-20200521152101746.png)

并且我们模板中的相应字段我们会存储在`VULN`表中

之后我们会利用`app.py`生成一个`index.html`，我们就可以通过`查看`功能来查看数据库内相应的字段，并且利用`Echarts`进行数据可视化过程

![image-20200521152214424](pic/README/image-20200521152214424.png)

## 配置安装

### 手工安装

#### Python

由于`OneForAll`基于[Python 3.8.0](https://www.python.org/downloads/release/python-380/)开发和测试，请使用高于Python 3.8.0的稳定发行版本，其他版本可能会出现一些问题（Windows平台必须使用3.8.0以上版本），安装Python环境可以参考[Python 3 安装指南](https://pythonguidecn.readthedocs.io/zh/latest/starting/installation.html#python-3)。运行以下命令检查Python和pip3版本：

```
python -V
pip3 -V
```

如果你看到以下类似输出便说明Python环境没有问题：

```
Python 3.8.0
pip 19.2.2 from C:\Users\shmilylty\AppData\Roaming\Python\Python38\site-packages\pip (python 3.8)
```

#### Git克隆部署

```
# Github地址
git clone https://github.com/Echocipher/AUTO-EARN
# Gitee地址（国内速度块）
git clone https://gitee.com/echocipher/AUTO-EARN
```

#### 依赖安装

```
cd AUTO-EARN/
python3 -m pip install -U pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### 相关配置

1. `chrome`请按照自己系统版本进行下载安装，放置在`./tools/chrome`中，或者在`./lib/config.py`中修改相应的位置，`crawlergo `只依赖`chrome`运行即可，前往[下载](https://www.chromium.org/getting-involved/download-chromium)新版本的`chromium`，或者直接[点击下载Linux79版本](https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/706915/chrome-linux.zip)。

   ![image-20200521160530503](pic/README/image-20200521160530503.png)

2. `OneForAll`相关配置在`./tools/OneForAll`目录中按照[OneForAll文档](https://github.com/shmilylty/OneForAll)按需进行个人配置即可

3. 在`./lib/config.py`中按照自己的需求对`server酱`、`shodan api`等进行配置

   ```
   '''
   AUTOEARN配置
   '''
   # 目标文件位置
   target_file_path = 'target.txt'
   # OneForAll相关配置
   oneforall_path = './tools/OneForAll/oneforall.py'
   # OneForAll数据库位置
   oneforall_sql_path = './tools/OneForAll/results/result.sqlite3'
   # Server酱SCKEY (http://sc.ftqq.com/?c=code)
   sckey = "https://sc.ftqq.com/{你的key}.send"
   # subdomain_status_check间隔时间
   server_sleep_time = 10
   # autoearn数据库位置
   result_sql_path = './results/result.sqlite3'
   #shodan API
   SHODAN_API_KEY = '{你的key}'
   # masscan位置
   masscan_path = './tools/masscan/bin/masscan'
   # masscan端口扫描范围
   masscan_port = '1-65535'
   # masscan临时文件保存位置
   masscan_file = './results/masscan.json'
   # masscan速率
   masscan_rate = '1000'
   # 端口最大数目阈值
   port_num_max = 50
   # wafw00f位置
   wafw00f_path = './tools/wafcheck/main.py'
   # crawlergo位置
   crawlergo_path = './tools/crawlergo'
   # chrome位置
   chrome_path = "./tools/chrome/chrome"
   # 爬虫同时开启最大标签页，即同时爬取的页面数量。
   max_tab_count = "20"
   # 发送爬虫结果到监听地址时的最大并发数
   max_send_count = "10"
   # Xray被动代理地址
   push_to_proxy = "http://127.0.0.1:7777"
   # 端口检查线程数
   port_check_thread_num = 10
   # 主页默认每页显示数目
   PER_PAGE = 10
   ```

4. `xray`配置按照[xray文档]([https://xray.cool/xray/#/tutorial/webscan_proxy?id=%e7%94%9f%e6%88%90-ca-%e8%af%81%e4%b9%a6](https://xray.cool/xray/#/tutorial/webscan_proxy?id=生成-ca-证书))根据个人系统进行`CA证书`配置以及`config.yml`配置

### Docker安装

## 使用说明

### 启动命令

```
cd AUTO-EARN/
sh start.sh
python3 autoearn.py
sh stop.sh
```

如果是`Windows`可自行构建`bat`来完成相应的过程，大致流程如下

1. 启动子域收集后，运行`python3 subdomain_monitor.py`

2. 漏洞扫描时运行如下命令

   ```
   python3 server.py
   ./tools/xray/xray_linux_amd64 webscan --listen 127.0.0.1:7777 --webhook-output http://127.0.0.1:2333/webhook
   ```

3. 也可以利用`>`实现相应的日志记录功能

4. 结束时终止如上进程以及备份`./results/result.sqlite3`以及清理`./tools/OneForAll/results`目录文件

### 参数说明

#### 1 - 获取子域

利用`oneforall`进行子域收集，收集过程中可以通过如下命令查看其中相应的日志信息

```
# 查看oneforall日志信息
tail -f logs/oneforall.log
```

![image-20200521174357261](pic/README/image-20200521174357261.png)

```
# 查看子域收集监控信息
tail -f logs/subdomain_monitor.log
```

![image-20200521174322059](pic/README/image-20200521174322059.png)

收集完成会收到相应通知，并且在数据库`SUBDOMAIN`表中进行相应存储

![image-20200521175401007](pic/README/image-20200521175401007.png)

#### 2 - 端口检测

![image-20200521175326338](pic/README/image-20200521175326338.png)

在子域收集完成后，我们就可以进行端口检测过程了，这里我们默认使用的是`shodan api`，默认线程数目为`10`，其中`masscan+nmap`代码已经加入其中，默认阈值是`50`，只需要进行简单的代码上的调整就可以完成应用，这里不做过多介绍，当端口检测完成后会像文初说的那样插入数据库中的`TASK`表

#### 3 - WAF检测

在上一部分任务数据库已经插入完成之后，程序会利用`wafw00f`对每个目标进行指纹识别，并且插入数据库中的`WAF`字段，我们可以在之后的`5 - 查看`时直观的看到结果



#### 4 - 爬虫爬取 + 漏洞探测 + 消息通知

该部分会像上面`工具流程`中说的那样自动化的完成页面链接的爬取以及发往被动扫描器的过程，`FUZZ`过程中我们可以使用如下命令查看相应日志信息

```
# 查看crawlergo日志信息
tail -f logs/crawlergo.log
# 查看xray日志信息
tail -f logs/xray.log
# 查看漏洞推送server信息
tail -f logs/server.log
```

当扫描到漏洞时，会利用`server酱`进行通知提醒，并且存储在数据库中`VULN`表中

![image-20200521181546824](pic/README/image-20200521181546824.png)

#### 5 - 查看

我们可以通过`查看`功能来起一个`web`服务，从而更方便的看到数据库中的内容，默认每页展示数为`5`，我们可以在`./lib/config.py`中修改这一限制，如果你是通过`手工安装`，你可以通过访问`http://127.0.0.1:5000`来查看这一页面，如果你是 `Docker安装`，你可以通过`Docker`命令将它映射到宿主机的相应端口上，上述配置教程中为转到`80`端口

![image-20200521183057853](pic/README/image-20200521183057853.png)

## 参考资源

1. [OneForAll - 一款功能强大的子域收集工具](https://github.com/shmilylty/OneForAll/)
2. [Shodan - Shodan is the world's first search engine for Internet-connected devices](https://www.shodan.io/)
3. [Crawlergo - 一个使用chrome headless模式进行URL入口收集的动态爬虫](https://github.com/0Kee-Team/crawlergo)
4. [Xray - 一款躺着收洞的神器](https://xray.cool/xray/#/)
5. [Rich - Rich is a Python library for rich text and beautiful formatting in the terminal](https://github.com/willmcgugan/rich)
6. [crawlergo_x_XRAY - 360/0Kee-Team/crawlergo动态爬虫结合长亭XRAY扫描器的被动扫描功能](https://github.com/timwhitez/crawlergo_x_XRAY)

