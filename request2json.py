from urllib.parse import parse_qsl
import json
'''
###### 将截获的post表单转成json格式 ######
'''

# 读取表单信息
with open("data/requestBody.txt", 'r') as f:
    s = f.read()
result = parse_qsl(s)

# 转成json格式表单信息
data = (dict(result))
jsonData = json.dumps(
    data, ensure_ascii=False, separators=(',', ':'))  # dumps：将python字典解码为json数据
with open("data/data.json", 'w',encoding='utf-8') as f:
    s = f.write(jsonData)
