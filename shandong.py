import requests
import re
import time
import json
import pandas as pd
import os, sys

# 伪装爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/64.0.3282.140 Safari/537.36 Edge/17.17134'
}
# 处理页码
data = {
    'colcode': '0303',
    'curpage': ''
}
ID0 = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/read.jsp?colcode=0303&id='
# 获取系统时间并命名cvs文件和excel文件
now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
file_name_cvs = r'G:/SK/python_work/' + now + r"_project.cvs"


# 处理单页的项目
def get_one_page(url):
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('发生错误!')
        return None


def parse_one_page(html):
    pattern = re.compile('<a.*?five.*?colcode=0303&id=(.*?)title.*?>(.*?)</a>.*?2018-(.*?)</td>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield (
            ID0 + item[0].strip().strip('\''),
            item[1].strip(),
            item[2]
        )


# 用正则表达式解析单页上的项目
# 用yield生成了字典等待被循环调用
# yield生成器避免了采用字典等处理大量数据时内存耗尽的问题，包含yield生成器的函数自动标为生成器函数，本质上属于特殊的迭代器,可以用next（）
# 进行调用，也可以用for循环


# 写入数据
def write_to_file(content):
    with open(file_name_cvs, 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # ensure_ascii=False 保证输出的是文字而不是二进制编码


def main(i):
    data['curpage'] = str(i)
    url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


# "Make a script both importable and executable”脚本模块既可以导入到别的模块中用，另外该模块自己也可执行
# 直接执行py文件if __name__ == '__main__'会被执行，从外部文件导入并执行mian（）时，此模块不会执行
if __name__ == '__main__':
    for i in range(1, 2):
        main(i)
        time.sleep(0.1)

for i in range(1, 60):
    main(i)
    time.sleep(0.1)
