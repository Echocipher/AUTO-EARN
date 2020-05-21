import time
import subprocess
from lib import config, server_push
from rich.console import Console


console = Console()


# 子域监控函数
def subdomain_status_check():
    while True:
        cmd = "ps -aux | grep oneforall.py | grep -v grep | awk '{print $2}'"
        console.log('正在进行子域收集监控')
        start_rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(config.server_sleep_time)
        end_rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if len(start_rsp.stdout.read().strip()) != 0:
            console.log('子域收集中')
            if len(end_rsp.stdout.read().strip()) == 0:
                server_push.subdomain_status_push()
                break



if __name__ == '__main__':
    subdomain_status_check()
