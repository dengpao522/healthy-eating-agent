import jieba

text = '中文分词是自然语言处理的一部分！'
# 全模式分词
seg_list = jieba.cut(text, cut_all=True)
print('全模式：', '/'.join(seg_list))
# 精确模式分词
seg_list = jieba.cut(text, cut_all=False)
print('精确模式：', '/'.join(seg_list))
# 搜索引擎模式分词
seg_list = jieba.cut_for_search(text)
print('搜索引擎模式：', '/'.join(seg_list))、


import re
def match_email_address(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

email1 = "test@example.com"
email2 = "invalid_email"
print(match_email_address(email1))  # 输出 True
print(match_email_address(email2))  # 输出 False

import re
def validate_phone_number(phone_number):
    pattern = r'^\d{3}-\d{8}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False

phone_number = '123-45678901'
if validate_phone_number(phone_number):
    print("电话号码格式正确")
else:
    print("电话号码格式不正确")

import re
def validate_date(date):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date):
        return True
    else:
        return False

date = '2023-10-27'
if validate_date(date):
    print("日期格式正确")
else:
    print("日期格式不正确")



import re
text = """
姓名: 张三
性别: 男
年龄: 25岁
电话号码: 13512345678
地址: 北京市朝阳区
"""

name_pattern = r"姓名: (.+?)\n"
gender_pattern = r"性别: (.+?)\n"
age_pattern = r"年龄: (.+?)岁\n"
phone_pattern = r"电话号码: (.+?)\n"
address_pattern = r"地址: (.+?)\n"

name = re.search(name_pattern, text).group(1)
gender = re.search(gender_pattern, text).group(1)
age = re.search(age_pattern, text).group(1)
phone = re.search(phone_pattern, text).group(1)
address = re.search(address_pattern, text).group(1)

print("姓名: ", name)
print("性别: ", gender)
print("年龄: ", age)
print("电话号码: ", phone)
print("地址: ", address)


import re
from urllib.request import urlopen
from opencc import OpenCC

url1 = 'http://***'  # 实际需替换为有效URL
html1 = urlopen(url1).read()
text4 = html1.decode('utf-8')
text_temp = text4[7406:7699]  # 截取部分文本（随网页更新可能需调整范围）

# 繁体转简体
converter = OpenCC('t2s')
simplified_text = converter.convert(text_temp)
print(simplified_text)