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
        reportUrl = "https://selfreport.shu.edu.cn/DayReport.aspx"  # 当日每日一报的网址

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
    }
    data.update(dataNew)
    header = {
        'X-FineUI-Ajax': 'true',
    }
    # application/x-www-form-urlencoded ==最常见的post提交数据的方式，以form表单形式提交数据
    response = requests.post(reportUrl, data=data,
                             cookies=cookie, headers=header)

    return response.text.find("提交成功")

# 获取网页默认选项信息


# def get_FState(reportData):
    # 读取文件信息
    # with open("requestBody.txt", 'r') as f:
    #     s = f.read()
    # result = parse_qsl(s)
    # F_STATE_Former_dict = (dict(result))

    # 变量修改
    # p1_BaoSRQ = reportData["date"].replace(" ", "")  # 这报送网站的变量名属实有点秀
    # p1_ddlSheng = reportData["province"]
    # p1_ddlShi = reportData["city"]
    # p1_ddlXian = reportData["county"]
    # p1_XiangXDZ = reportData["location"]

    # F_STATE_Former_dict['p1_BaoSRQ'].update({'Text': p1_BaoSRQ})
    # F_STATE_Former_dict['p1_ddlSheng'].update(
    #     {'SelectedValueArray': [p1_ddlSheng]})
    # F_STATE_Former_dict['p1_ddlShi'].update(
    #     {'SelectedValueArray': [p1_ddlShi]})
    # F_STATE_Former_dict['p1_ddlXian'].update(
    #     {'SelectedValueArray': [p1_ddlXian]})
    # F_STATE_Former_dict['p1_XiangXDZ'].update({'Text': p1_XiangXDZ})
    # 修改变量以后再编码
    # F_State_New_str = json.dumps(
    #     F_STATE_Former_dict, ensure_ascii=False, separators=(',', ':'))  # dumps：将python对象解码为json数据

    # with open("data.txt", 'w', encoding='utf-8') as f:
    #     s = f.write(F_State_New_str)
    # F_State_New = base64.b64encode(F_State_New_str.encode("utf-8")).decode()
    # return F_State_New


if __name__ == "__main__":
    # studentId = sys.argv[1]
    # password = sys.argv[2]
    studentId = '18122836'
    password = 'ymzYMZ145'
    studentInfoList = [[studentId, password]]

    timeUTC = datetime.datetime.utcnow()
    timeLocal = timeUTC + datetime.timedelta(hours=8)
    date = timeLocal.strftime('%Y - %m - %d')
    if(timeLocal.hour >= 19):
        Time_1or2 = "2"
    else:
        Time_1or2 = "1"

    reportData = {"date": date,
                  "province": "安徽",
                  "city": "合肥市",
                  "county": "肥东县",
                  "location": "撮镇镇红旗路东城家园小区"}

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
