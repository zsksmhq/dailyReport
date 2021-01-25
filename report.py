# -*- coding:UTF-8 -*-
import sys
import requests
import report_leave_school
import report_at_school

def get_cookies(studentInfo):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }
    loginUrl = "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MDY2NTA3MzEzODc1NDIzODYsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmIiwic3RhdGUiOiIifQ=="
    data = {"username": studentInfo[0],
            "password": studentInfo[1],
            }
    response = requests.post(loginUrl, headers=header, data=data, allow_redirects=False)
    response = requests.get("https://newsso.shu.edu.cn" + response.headers["location"], cookies=response.cookies,
                            allow_redirects=False)
    response = requests.get(response.headers["location"], allow_redirects=False)
    return (response.cookies)


if (__name__ == "__main__"):
    url = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    studentId = sys.argv[1]
    password = sys.argv[2]
    studentInfo = [studentId, password]
    cookie = get_cookies(studentInfo)
    try:
        cookie = get_cookies(studentInfo)
    except:
        print("无法获取学号  " + studentInfo[0] + "  的cookie,可能是账号密码错误")
    else:
        response = requests.get(url=url,headers=header,cookies=cookie)  #通过跳转地址是每日一报还是两报来判断是否在校
        if (response.url=="https://selfreport.shu.edu.cn/DayReport.aspx"):
            report_leave_school.main(cookie)
        elif (response.url==url):
            report_at_school.main(cookie)
