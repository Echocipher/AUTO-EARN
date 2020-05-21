import sys
from rich.console import Console


console = Console()


# 读取文件函数
def read_target(file):
	url_list = []
	try:
		with open(file,'r') as wr:
			for url in wr.readlines():
				url_list.append(url.strip()) # 把末尾的'\n'删掉
		return url_list
	except:
		console.print('目标文件读取异常，请检查文件是否存在', style="bold red")
		sys.exit()


