import sys
import time
import shodan
from lib import config, subdomain_collect, run_html,  waf_check, sql_connect, craw_to_xray
from lib.read_target import read_target
from rich.console import Console
from rich.table import Column, Table

console = Console()


# banner生成函数
def banner():
    msg = '''

     ▄▄▄       █    ██ ▄▄▄█████▓ ▒█████     ▓█████ ▄▄▄       ██▀███   ███▄    █    
    ▒████▄     ██  ▓██▒▓  ██▒ ▓▒▒██▒  ██▒   ▓█   ▀▒████▄    ▓██ ▒ ██▒ ██ ▀█   █    
    ▒██  ▀█▄  ▓██  ▒██░▒ ▓██░ ▒░▒██░  ██▒   ▒███  ▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▀█ ██▒   
    ░██▄▄▄▄██ ▓▓█  ░██░░ ▓██▓ ░ ▒██   ██░   ▒▓█  ▄░██▄▄▄▄██ ▒██▀▀█▄  ▓██▒  ▐▌██▒ 
     ▓█   ▓██▒▒▒█████▓   ▒██▒ ░ ░ ████▓▒░   ░▒████▒▓█   ▓██▒░██▓ ▒██▒▒██░   ▓██░   
     ▒▒   ▓▒█░░▒▓▒ ▒ ▒   ▒ ░░   ░ ▒░▒░▒░    ░░ ▒░ ░▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒    
      ▒   ▒▒ ░░░▒░ ░ ░     ░      ░ ▒ ▒░     ░ ░  ░ ▒   ▒▒ ░  ░▒ ░ ▒░░ ░░   ░ ▒░   
      ░   ▒    ░░░ ░ ░   ░      ░ ░ ░ ▒        ░    ░   ▒     ░░   ░    ░   ░ ░    
          ░  ░   ░                  ░ ░        ░  ░     ░  ░   ░              ░  
    '''

    console.print(msg, style="bold red")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ABOUT", style="dim", width=30)
    table.add_column("AUTHOR", style="dim", width=30)
    table.add_column("PLUGINS", style="dim", width=30)
    help_table = Table(show_header=True, header_style="bold magenta")
    help_table.add_column("ID", style="dim", width=30)
    help_table.add_column("参数", style="dim", width=30)
    help_table.add_column("说明", style="dim", width=30)
    table.add_row(
    "一款SRC漏洞挖掘辅助工具",
    "Echocipher",
    "OneForAll"
    )
    table.add_row(
    "",
    "",
    "Masscan"
    )
    table.add_row(
    "",
    "",
    "Nmap"
    )
    table.add_row(
    "",
    "",
    "Wafw00f"
    )
    table.add_row(
    "",
    "",
    "Crawlergo"
    )    
    table.add_row(
    "",
    "",
    "Xray"
    )
    help_table.add_row(
    "1",
    "Subdomain_Collect",
    "获取子域"
    )
    help_table.add_row(
    "2",
    "Port_Check",
    "端口检测"
    )
    help_table.add_row(
    "3",
    "Waf_Check",
    "WAF检测"
    )
    help_table.add_row(
    "4",
    "Craw_To_Xray",
    "爬虫爬取 + 漏洞探测 + 消息通知"
    )
    help_table.add_row(
    "5",
    "View",
    "查看"
    )
    help_table.add_row(
    "6",
    "Exit",
    "退出"
    )
    console.print(table)
    console.print('参数说明', style="#ADFF2F")
    console.print(help_table)


# 结束函数
def end():
    console.print("shutting down at {0}".format(time.strftime("%X")), style="#ADFF2F")


def main():
    banner()
    while True:
        console.print('请输入要执行的参数ID：[bold cyan]1-6[/bold cyan]', style="#ADFF2F")
        args = input('> ')
        if args == '1':
            subdomain_collect.oneforall_collect(config.target_file_path)
        elif args == '2':
            try:
                SHODAN_API_KEY = config.SHODAN_API_KEY
                api = shodan.Shodan(SHODAN_API_KEY)
                api.info()
                console.print('Shodan密钥验证成功', style="#ADFF2F")
                from lib import port_check
            except:
                console.print('Shodan密钥验证失败',style="bold red")
                sys.exit()
        elif args == '3':
            waf_check.waf_check(sql_connect.read_task_sql())
        elif args == '4':
            craw_to_xray.craw_to_xray(sql_connect.read_task_sql())
        elif args == '5':
            run_html.main()
        elif args == '6':
            break
        else:
            console.print('输入参数有误，请检查后输入', style="bold red")
            sys.exit()
    end()


if __name__ == '__main__':
    main()