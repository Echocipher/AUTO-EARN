import socket
from rich.console import Console


console = Console()


# 判断CDN函数
def check_cdn(domain):
    ip_list = []
    try:
        console.print('正在进行CDN检测', style="#ADFF2F")
        addrs = socket.getaddrinfo(domain, None, family=0)
        for item in addrs:
            if item[4][0] not in ip_list:
                if item[4][0].count('.') == 3:
                    ip_list.append(item[4][0])
                else:
                    pass
        return ip_list
    except:
        console.print('CDN检测失败，请检查输入格式', style="bold red")
        pass



        