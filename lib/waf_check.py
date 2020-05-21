import json
import sqlite3
import subprocess
from lib import config
from rich.console import Console


console = Console()


# WAF检测函数
def waf_check(domain_list):
    console.print('正在进行WAF检测',style="#ADFF2F")
    console.print('任务数据库连接成功',style="#ADFF2F")
    conn = sqlite3.connect(config.result_sql_path)
    c = conn.cursor()
    for domain in domain_list:
        domain = domain[1]
        cmd = ['python3', config.wafw00f_path, domain]
        rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for i in (rsp.stdout.read().decode("GBK").split('\n')):
            if 'url' in i:
                url = json.loads(i.replace('\'', '\"'))['url']
                waf = json.loads(i.replace('\'', '\"'))['waf'][0]
                c.execute("UPDATE TASK set WAF = '%s' where URL = '%s' "%(waf, url))
                c.execute("UPDATE TASK set STATUS = 'WAF检测完成' where URL = '%s' "%(url,))
                conn.commit()
        while True:
            if rsp.poll() == None:
                pass
            else:
                break
    console.print('WAF检测完成',style="#ADFF2F")
    conn.close()