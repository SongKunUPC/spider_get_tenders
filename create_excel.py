# coding = uft-8
import pandas as pd
import time
import json
import sys, os


now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
file_name_cvs = r'G:/SK/python_work/' + now + r"_project.cvs"
file_name_xls = r'G:/SK/python_work/' + now + r"_project.xls"
df = pd.read_csv(file_name_cvs, encoding='utf-8', names=['ID', 'Title', 'Date'])
# 筛选项目中含有的关键词
bl = df.Title.str.contains('第三方|督导|评估|质量监测|办学质量|办学水平|教育局|发展规划')
filter_df = df[bl]
filter_df.to_excel(file_name_xls)
