import requests
import re
import time
import json
import pandas as pd
import os, sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/64.0.3282.140 Safari/537.36 Edge/17.17134'
}
url0 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=2&pageSize=10&pageNo='
ID0 = 'http://www.hngp.gov.cn/henan/content'
# 获取系统时间并命名cvs文件和excel文件
now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
file_name_cvs = r'G:/SK/python_work/' + now + r"_project.cvs"


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('发生错误!')
        return None


def parse_one_page(html):
    pattern = re.compile('<li><span class="Right Gray">(.*?)</span><a.*?href="/henan/content(.*?)">(.*?)</a>.*?</li>',
                         re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield (
            ID0 + item[1].strip(),
            item[2],
            item[0]
        )


def write_to_file(content):
    with open(file_name_cvs, 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # ensure_ascii=False 保证输出的是文字而不是二进制编码


def main(i):
    url = url0 + str(i)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(1, 2):
        main(i)
        time.sleep(0.1)

for i in range(1, 60):
    main(i)
    time.sleep(0.1)