import requests
import datetime
from bs4 import BeautifulSoup
import base64
import json
import random
import sys


# 获取cookies
def get_cookies(studentInfo):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
              }
    loginUrl = "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MDY2NTA3MzEzODc1NDIzODYsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmIiwic3RhdGUiOiIifQ=="
    data = {"username": studentInfo[0],
            "password": studentInfo[1],
            }
    response = requests.post(loginUrl, headers=header,
                             data=data, allow_redirects=False)
    response = requests.get("https://newsso.shu.edu.cn" +
                            response.headers["location"], cookies=response.cookies, allow_redirects=False)
    response = requests.get(
        response.headers["location"], allow_redirects=False)
    return (response.cookies)


# 提交数据
def daily_report(cookie, reportData, delayReport=False):  # 最后个参数是补报用的

    if(delayReport == True):
        reportUrl = "https://selfreport.shu.edu.cn/DayReport.aspx"  # 补报的网址
    else:
        reportUrl = "https://selfreport.shu.edu.cn/DayReport.aspx"  # 当天每日一报的网址

    # 获取网页基本信息(get)
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
              }

    # 读取表单信息
    with open("data/data.json", 'r', encoding='utf-8') as f:
        dataString = f.read()
    data = json.loads(dataString)
    # 更新表单信息
    dataNew = {
        "p1$BaoSRQ": reportData["date"],
        "p1$ddlSheng$Value": reportData["province"],
        "p1$ddlSheng": reportData["province"],
        "p1$ddlShi$Value": reportData["city"],
        "p1$ddlShi": reportData["city"],
        "p1$ddlXian$Value": reportData["county"],
        "p1$ddlXian": reportData["county"],
        "p1$XiangXDZ": reportData["location"],
        "F_STATE":get_FState(reportData)
    }
    data.update(dataNew)
    header = {
        'X-FineUI-Ajax': 'true',
    }
    # application/x-www-form-urlencoded ==最常见的post提交数据的方式，以form表单形式提交数据
    response = requests.post(reportUrl, data=data,
                             cookies=cookie, headers=header)

    return response.text.find("提交成功")

# 更新F_STATE数据
def get_FState(reportData):

    # 读取F_STATE初始信息
    with open("data/data.json", 'r', encoding='utf-8') as f:
        dataString = f.read()
    dataDicts = json.loads(dataString)
    F_State_String = dataDicts["F_STATE"]

    # 解码
    F_State_Former_str = str(base64.b64decode(
        F_State_String), encoding='utf-8')
    F_STATE_Former_dict = json.loads(F_State_Former_str)

    # 转成json格式并保存（方便查看）
    jsonData = json.dumps(
        F_STATE_Former_dict, ensure_ascii=False, separators=(',', ':'))  # dumps：将python字典解码为json数据
    # with open("data/F_State.json", 'w', encoding='utf-8') as f:
    #     s = f.write(jsonData)

    # 更新数据
    F_State_New_dict = {
        "p1_BaoSRQ": {
            "Text": reportData["date"].replace(" ", "")
        },
        "p1_ddlSheng": {
            "SelectedValueArray": [reportData["province"]]
        },
        "p1_ddlShi": {
            "SelectedValueArray": [reportData["city"]]
        },
        "p1_ddlXian": {
            "SelectedValueArray": [reportData["county"]]
        },
        "p1_XiangXDZ": {
            "SelectedValueArray": [reportData["location"]]
        },
    }
    F_STATE_Former_dict.update(F_State_New_dict)

    # 编码
    F_State_NewString = base64.b64encode(jsonData.encode("utf-8")).decode()

    return F_State_NewString


if __name__ == "__main__":
    # 学生信息
    studentId = sys.argv[1]
    password = sys.argv[2]
    studentInfoList = [[studentId, password]]
    # 地点信息
    location = sys.argv[3].split(',')

    # 获取时间
    timeUTC = datetime.datetime.utcnow()
    timeLocal = timeUTC + datetime.timedelta(hours=8)
    date = timeLocal.strftime('%Y - %m - %d')
    # 提交的信息
    reportData = {"date": date,
                  "province": location[0],
                  "city": location[1],
                  "county": location[2],
                  "location": location[3]}

    for studentInfo in studentInfoList:
        try:
            cookie = get_cookies(studentInfo)
        except:
            print("无法获取学号  " + studentInfo[0] + "  的cookie,可能是账号密码错误")
            continue
        reportSuccess = daily_report(cookie, reportData)
        if (reportSuccess) == -1:
            print(str(studentInfo[0] + "   报送失败"))
        else:
            print(str(studentInfo[0] + "   提交成功"))
