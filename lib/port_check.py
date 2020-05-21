import sys
import nmap
import json
import shodan
import subprocess
from lib import config
from lib import sql_connect, check_cdn
from rich.console import Console
from rich.progress import track


console = Console()


# shodan获取端口、服务
def shodan_port_check(ip,domain):
    url_list = []
    SHODAN_API_KEY = config.SHODAN_API_KEY
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        results = api.host(ip)
        ports = results['ports']
        datas = results['data']
        for data in datas:
            port = data['port']
            module = data['_shodan']['module']
            if 'http' in module:
                if 'https' in module:
                    url = 'https://' + domain + ':' + str(port)
                else:
                    url = 'http://' + domain + ':' + str(port)
                url_list.append(url)
    except:
        console.print('目标' + domain + '查询失败，已跳过', style="bold red")
    return url_list


# masscan端口检测函数
def masscan_port_check(ip):
    tmp_list = []
    url_list = []
    results_list = []
    console.print('正在进行端口探测', style="#ADFF2F")
    # cmd = ['sudo', config.masscan_path, ip, '-p', config.masscan_port, '-oJ', config.masscan_file, '--rate', config.masscan_rate]
    cmd = 'sudo ' + config.masscan_path + " " + ip + ' -p ' + config.masscan_port + ' -oJ ' +  config.masscan_file + ' --rate '+ config.masscan_rate
    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while True:
        if rsp.poll() == None:
            pass
        else:
            break
    with open (config.masscan_file, 'r') as wr:
        for line in json.loads(wr.read()):
            ip = line['ip']
            port = line['ports'][0]['port']
            result_dict = {
                'ip':ip,
                'port':port
            }
            tmp_list.append(result_dict)
        if len(tmp_list) > config.port_num_max:
            tmp_list.clear()
        else:
            results_list.extend(tmp_list)
        for result in results_list:
            ip = result['ip']
            port = str(result['port'])
            url = service_check(ip,port)
            if len(url) > 0:
                url_list.append(url)
        return url_list


# service检测函数
def service_check(ip,port):
    url_list = []
    nm = nmap.PortScanner()
    ret = nm.scan(ip,port, arguments = '-Pn,-sS')
    service_name = ret['scan'][ip]['tcp'][int(port)]['name']
    if 'http' in service_name or service_name == 'sun-answerbook':
        if service_name == 'https' or service_name == 'https-alt':
            url = 'https://' + ip + ':' + port
        else:
            url = 'http://' + ip + ':' + port
        return url


# 判断subdomain cdn
def subdomain_port_check():  
    url_list = []
    for domain in track(sql_connect.read_subdomain_sql()):
        try:
            if len(check_cdn.check_cdn(domain[1])) == 1:
                url_list.extend(shodan_port_check(check_cdn.check_cdn(domain[1])[0],domain[1]))
            else:
                console.print('目标存在CDN', style="bold red")
                url_list.append('http://'+domain[1])
        except:
            console.print('目标' + domain[1] + '查询异常', style="bold red")
    sql_connect.insert_task_sql(url_list)


import queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        console.print("开启线程：" + self.name, style="#ADFF2F")
        mul_subdomain_port_check(self.name, self.q)
        console.print("退出线程：" + self.name, style="#ADFF2F")


def mul_subdomain_port_check(threadName, q):
    url_list = []
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            domain = q.get()
            queueLock.release()
            try:
                if len(check_cdn.check_cdn(domain[1])) == 1:
                    url_list.extend(shodan_port_check(check_cdn.check_cdn(domain[1])[0],domain[1]))
                else:
                    console.print('目标存在CDN', style="bold red")
                    url_list.append('http://'+domain[1])
            except:
                console.print('目标' + domain[1] + '查询异常', style="bold red")
            console.print("%s processing %s" % (threadName, domain[1]), style="#ADFF2F")
        else:
            queueLock.release()
    sql_connect.insert_task_sql(url_list)

threadNum = config.port_check_thread_num
threadList = []
for th in range(threadNum):
    threadList.append("Thread-"+str(th))
domainList = sql_connect.read_subdomain_sql()
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for domain in domainList:
    workQueue.put(domain)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
console.print('退出主线程', style="#ADFF2F")