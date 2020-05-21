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