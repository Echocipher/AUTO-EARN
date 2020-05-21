import subprocess
from lib import config
from rich.console import Console


console = Console()

# 子域收集函数
def oneforall_collect(target):
    cmd = 'nohup python3 ' + config.oneforall_path + ' --target ' + target + ' run > logs/oneforall.log 2>&1 &'
    try:
	    rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	    console.print('正在后台进行子域收集', style="#ADFF2F")
    except:
        console.print('子域收集失败，请检查输入格式', style="bold red")


