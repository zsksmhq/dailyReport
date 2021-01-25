import requests
import datetime
from bs4 import BeautifulSoup
import base64
import json
import random
import sys

def get_cookies(studentInfo):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    loginUrl = "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MDY2NTA3MzEzODc1NDIzODYsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmIiwic3RhdGUiOiIifQ=="
    data = {"username": studentInfo[0],
            "password": studentInfo[1],
    }
    response = requests.post(loginUrl,headers=header,data=data,allow_redirects=False)
    response = requests.get("https://newsso.shu.edu.cn" + response.headers["location"], cookies=response.cookies,allow_redirects=False)
    response = requests.get(response.headers["location"],allow_redirects=False)
    return (response.cookies)



def daily_report(cookie,reportData,delayReport = False):  #最后个参数是补报用的
    if(delayReport==False):
        reportUrl = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=" + reportData["Time_1or2"]
    else:
        reportUrl = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day="+ reportData["date"].replace(" ","") + "t=" + reportData["Time_1or2"]
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    response = requests.get(reportUrl, cookies=cookie)
    soup = BeautifulSoup(response.text, 'html.parser')
    view_state = soup.find('input', attrs={'name': '__VIEWSTATE'})
    data = {
        "__EVENTTARGET": "p1$ctl00$btnSubmit",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": view_state['value'],
        "__VIEWSTATEGENERATOR": "DC4D08A3",
        "p1$ChengNuo": "p1_ChengNuo",
        "p1$BaoSRQ": reportData["date"],
        "p1$DangQSTZK": "良好",
        "p1$TiWen": reportData["temperature"],
        "p1$ZaiXiao": reportData["campusLocation"],
        "p1$ddlSheng$Value": "上海",
        "p1$ddlSheng": "上海",
        "p1$ddlShi$Value": "上海市",
        "p1$ddlShi": "上海市",
        "p1$ddlXian$Value": reportData["county"],
        "p1$ddlXian": reportData["county"],
        "p1$FengXDQDL": "否",
        "p1$TongZWDLH": "否",
        "p1$XiangXDZ": reportData["location"],
        "p1$QueZHZJC$Value": "否",
        "p1$QueZHZJC": "否",
        "p1$DangRGL": "否",
        "p1$GeLDZ": "",
        "p1$CengFWH": "否",
        "p1$CengFWH_RiQi": "",
        "p1$CengFWH_BeiZhu": "",
        "p1$JieChu": "否",
        "p1$JieChu_RiQi": "",
        "p1$JieChu_BeiZhu": "",
        "p1$TuJWH": "否",
        "p1$TuJWH_RiQi": "",
        "p1$TuJWH_BeiZhu": "",
        "p1$JiaRen_BeiZhu": "",
        "p1$SuiSM": "绿色",
        "p1$LvMa14Days": "是",
        "p1$Address2": "",
        "F_TARGET": "p1_ctl00_btnSubmit",
        "p1_GeLSM_Collapsed": "false",
        "p1_Collapsed": "false",
        'F_STATE': get_FState(reportData),
    }
    header = {
        'X-FineUI-Ajax': 'true',
    }
    response = requests.post(reportUrl, data=data, cookies=cookie,headers=header)
    return response.text.find("提交成功")


def get_FState(reportData):
    F_STATE_Former = "eyJwMV9CYW9TUlEiOnsiVGV4dCI6IjIwMjAtMTEtMjkifSwicDFfRGFuZ1FTVFpLIjp7IkZfSXRlbXMiOltbIuiJr+WlvSIsIuiJr+WlvSIsMV0sWyLkuI3pgIIiLCLkuI3pgIIiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuiJr+WlvSJ9LCJwMV9aaGVuZ1podWFuZyI6eyJIaWRkZW4iOnRydWUsIkZfSXRlbXMiOltbIuaEn+WGkiIsIuaEn+WGkiIsMV0sWyLlkrPll70iLCLlkrPll70iLDFdLFsi5Y+R54OtIiwi5Y+R54OtIiwxXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6W119LCJwMV9UaVdlbiI6eyJUZXh0IjoiMzcuMCJ9LCJwMV9aYWlYaWFvIjp7IlNlbGVjdGVkVmFsdWUiOiLlrp3lsbEiLCJGX0l0ZW1zIjpbWyLkuI3lnKjmoKEiLCLkuI3lnKjmoKEiLDFdLFsi5a6d5bGxIiwi5a6d5bGx5qCh5Yy6IiwxXSxbIuW7tumVvyIsIuW7tumVv+agoeWMuiIsMV0sWyLlmInlrpoiLCLlmInlrprmoKHljLoiLDFdLFsi5paw6Ze46LevIiwi5paw6Ze46Lev5qCh5Yy6IiwxXV19LCJwMV9kZGxTaGVuZyI6eyJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeecgeS7vSIsMSwiIiwiIl0sWyLljJfkuqwiLCLljJfkuqwiLDEsIiIsIiJdLFsi5aSp5rSlIiwi5aSp5rSlIiwxLCIiLCIiXSxbIuS4iua1tyIsIuS4iua1tyIsMSwiIiwiIl0sWyLph43luoYiLCLph43luoYiLDEsIiIsIiJdLFsi5rKz5YyXIiwi5rKz5YyXIiwxLCIiLCIiXSxbIuWxseilvyIsIuWxseilvyIsMSwiIiwiIl0sWyLovr3lroEiLCLovr3lroEiLDEsIiIsIiJdLFsi5ZCJ5p6XIiwi5ZCJ5p6XIiwxLCIiLCIiXSxbIum7kem+meaxnyIsIum7kem+meaxnyIsMSwiIiwiIl0sWyLmsZ/oi48iLCLmsZ/oi48iLDEsIiIsIiJdLFsi5rWZ5rGfIiwi5rWZ5rGfIiwxLCIiLCIiXSxbIuWuieW+vSIsIuWuieW+vSIsMSwiIiwiIl0sWyLnpo/lu7oiLCLnpo/lu7oiLDEsIiIsIiJdLFsi5rGf6KW/Iiwi5rGf6KW/IiwxLCIiLCIiXSxbIuWxseS4nCIsIuWxseS4nCIsMSwiIiwiIl0sWyLmsrPljZciLCLmsrPljZciLDEsIiIsIiJdLFsi5rmW5YyXIiwi5rmW5YyXIiwxLCIiLCIiXSxbIua5luWNlyIsIua5luWNlyIsMSwiIiwiIl0sWyLlub/kuJwiLCLlub/kuJwiLDEsIiIsIiJdLFsi5rW35Y2XIiwi5rW35Y2XIiwxLCIiLCIiXSxbIuWbm+W3nSIsIuWbm+W3nSIsMSwiIiwiIl0sWyLotLXlt54iLCLotLXlt54iLDEsIiIsIiJdLFsi5LqR5Y2XIiwi5LqR5Y2XIiwxLCIiLCIiXSxbIumZleilvyIsIumZleilvyIsMSwiIiwiIl0sWyLnlJjogoMiLCLnlJjogoMiLDEsIiIsIiJdLFsi6Z2S5rW3Iiwi6Z2S5rW3IiwxLCIiLCIiXSxbIuWGheiSmeWPpCIsIuWGheiSmeWPpCIsMSwiIiwiIl0sWyLlub/opb8iLCLlub/opb8iLDEsIiIsIiJdLFsi6KW/6JePIiwi6KW/6JePIiwxLCIiLCIiXSxbIuWugeWkjyIsIuWugeWkjyIsMSwiIiwiIl0sWyLmlrDnloYiLCLmlrDnloYiLDEsIiIsIiJdLFsi6aaZ5rivIiwi6aaZ5rivIiwxLCIiLCIiXSxbIua+s+mXqCIsIua+s+mXqCIsMSwiIiwiIl0sWyLlj7Dmub4iLCLlj7Dmub4iLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuS4iua1tyJdfSwicDFfZGRsU2hpIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5biCIiwxLCIiLCIiXSxbIuS4iua1t+W4giIsIuS4iua1t+W4giIsMSwiIiwiIl1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOlsi5LiK5rW35biCIl19LCJwMV9kZGxYaWFuIjp7IkVuYWJsZWQiOnRydWUsIkZfSXRlbXMiOltbIi0xIiwi6YCJ5oup5Y6/5Yy6IiwxLCIiLCIiXSxbIum7hOa1puWMuiIsIum7hOa1puWMuiIsMSwiIiwiIl0sWyLljaLmub7ljLoiLCLljaLmub7ljLoiLDEsIiIsIiJdLFsi5b6Q5rGH5Yy6Iiwi5b6Q5rGH5Yy6IiwxLCIiLCIiXSxbIumVv+WugeWMuiIsIumVv+WugeWMuiIsMSwiIiwiIl0sWyLpnZnlronljLoiLCLpnZnlronljLoiLDEsIiIsIiJdLFsi5pmu6ZmA5Yy6Iiwi5pmu6ZmA5Yy6IiwxLCIiLCIiXSxbIuiZueWPo+WMuiIsIuiZueWPo+WMuiIsMSwiIiwiIl0sWyLmnajmtabljLoiLCLmnajmtabljLoiLDEsIiIsIiJdLFsi5a6d5bGx5Yy6Iiwi5a6d5bGx5Yy6IiwxLCIiLCIiXSxbIumXteihjOWMuiIsIumXteihjOWMuiIsMSwiIiwiIl0sWyLlmInlrprljLoiLCLlmInlrprljLoiLDEsIiIsIiJdLFsi5p2+5rGf5Yy6Iiwi5p2+5rGf5Yy6IiwxLCIiLCIiXSxbIumHkeWxseWMuiIsIumHkeWxseWMuiIsMSwiIiwiIl0sWyLpnZLmtabljLoiLCLpnZLmtabljLoiLDEsIiIsIiJdLFsi5aWJ6LSk5Yy6Iiwi5aWJ6LSk5Yy6IiwxLCIiLCIiXSxbIua1puS4nOaWsOWMuiIsIua1puS4nOaWsOWMuiIsMSwiIiwiIl0sWyLltIfmmI7ljLoiLCLltIfmmI7ljLoiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuWuneWxseWMuiJdfSwicDFfRmVuZ1hEUURMIjp7IlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9Ub25nWldETEgiOnsiU2VsZWN0ZWRWYWx1ZSI6IuWQpiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXX0sInAxX1hpYW5nWERaIjp7IlRleHQiOiLljZcxNCJ9LCJwMV9RdWVaSFpKQyI6eyJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDEsIiIsIiJdLFsi5ZCmIiwi5ZCmIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLlkKYiXX0sInAxX0RhbmdSR0wiOnsiU2VsZWN0ZWRWYWx1ZSI6IuWQpiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXX0sInAxX0dlTFNNIjp7IkhpZGRlbiI6dHJ1ZSwiSUZyYW1lQXR0cmlidXRlcyI6e319LCJwMV9HZUxGUyI6eyJSZXF1aXJlZCI6ZmFsc2UsIkhpZGRlbiI6dHJ1ZSwiRl9JdGVtcyI6W1si5bGF5a626ZqU56a7Iiwi5bGF5a626ZqU56a7IiwxXSxbIumbhuS4remalOemuyIsIumbhuS4remalOemuyIsMV1dLCJTZWxlY3RlZFZhbHVlIjpudWxsfSwicDFfR2VMRFoiOnsiSGlkZGVuIjp0cnVlfSwicDFfQ2VuZ0ZXSCI6eyJMYWJlbCI6IjIwMjDlubQ55pyIMjfml6XlkI7mmK/lkKblnKjkuK3pq5jpo47pmanlnLDljLrpgJfnlZnov4c8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5aSp5rSl5Lic55aG5riv5Yy6556w5rW36L2p5bCP5Yy644CB5rWm5Lic5ZGo5rWm6ZWH5piO5aSp5Y2O5Z+O5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH5paw55Sf5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH6Iiq5Z+O5LiD6LevNDUw5byE5bCP5Yy644CB5rWm5Lic5byg5rGf6ZWH6aG65ZKM6LevMTI25byE5bCP5Yy644CB5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT5Yqe5LqL5aSE44CB5YaF6JKZ5Y+k5ruh5rSy6YeM5YyX5Yy66KGX6YGT77yJPC9zcGFuPiIsIkZfSXRlbXMiOltbIuaYryIsIuaYryIsMV0sWyLlkKYiLCLlkKYiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuWQpiJ9LCJwMV9DZW5nRldIX1JpUWkiOnsiSGlkZGVuIjp0cnVlfSwicDFfQ2VuZ0ZXSF9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfSmllQ2h1Ijp7IkxhYmVsIjoiMTHmnIgxNeaXpeiHszEx5pyIMjnml6XmmK/lkKbkuI7mnaXoh6rkuK3pq5jpo47pmanlnLDljLrlj5Hng63kurrlkZjlr4bliIfmjqXop6Y8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5aSp5rSl5Lic55aG5riv5Yy6556w5rW36L2p5bCP5Yy644CB5rWm5Lic5ZGo5rWm6ZWH5piO5aSp5Y2O5Z+O5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH5paw55Sf5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH6Iiq5Z+O5LiD6LevNDUw5byE5bCP5Yy644CB5rWm5Lic5byg5rGf6ZWH6aG65ZKM6LevMTI25byE5bCP5Yy644CB5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT5Yqe5LqL5aSE44CB5YaF6JKZ5Y+k5ruh5rSy6YeM5YyX5Yy66KGX6YGT77yJPC9zcGFuPiIsIlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9KaWVDaHVfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWVDaHVfQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIIjp7IkxhYmVsIjoiMTHmnIgxNeaXpeiHszEx5pyIMjnml6XmmK/lkKbkuZjlnZDlhazlhbHkuqTpgJrpgJTlvoTkuK3pq5jpo47pmanlnLDljLo8c3BhbiBzdHlsZT0nY29sb3I6cmVkOyc+77yI5aSp5rSl5Lic55aG5riv5Yy6556w5rW36L2p5bCP5Yy644CB5rWm5Lic5ZGo5rWm6ZWH5piO5aSp5Y2O5Z+O5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH5paw55Sf5bCP5Yy644CB5rWm5Lic56Wd5qGl6ZWH6Iiq5Z+O5LiD6LevNDUw5byE5bCP5Yy644CB5rWm5Lic5byg5rGf6ZWH6aG65ZKM6LevMTI25byE5bCP5Yy644CB5YaF6JKZ5Y+k5ruh5rSy6YeM5Lic5bGx6KGX6YGT5Yqe5LqL5aSE44CB5YaF6JKZ5Y+k5ruh5rSy6YeM5YyX5Yy66KGX6YGT77yJPC9zcGFuPiIsIlNlbGVjdGVkVmFsdWUiOiLlkKYiLCJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8iLDFdLFsi5ZCmIiwi5ZCmIiwxXV19LCJwMV9UdUpXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIxMeaciDE15pel6IezMTHmnIgyOeaXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtiJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxX1N1aVNNIjp7IlNlbGVjdGVkVmFsdWUiOiLnu7/oibIiLCJGX0l0ZW1zIjpbWyLnuqLoibIiLCLnuqLoibIiLDFdLFsi6buE6ImyIiwi6buE6ImyIiwxXSxbIue7v+iJsiIsIue7v+iJsiIsMV1dfSwicDFfTHZNYTE0RGF5cyI6eyJTZWxlY3RlZFZhbHVlIjoi5pivIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDEiOnsiVGl0bGUiOiLmr4/ml6XkuKTmiqXvvIjkuIrljYjvvIkiLCJJRnJhbWVBdHRyaWJ1dGVzIjp7fX19"
    if reportData["Time_1or2"] == "1" : p1 = "每日两报（上午）"
    if reportData["Time_1or2"] == "2" : p1 = "每日两报（下午）"
    p1_BaoSRQ = reportData["date"].replace(" ","")   #这报送网站的变量名属实有点秀
    p1_TiWen = reportData["temperature"]
    p1_ZaiXiao = reportData["campusLocation"]
    p1_ddlXian = reportData["county"]
    p1_XiangXDZ = reportData["location"]
    F_State_Former_str = str(base64.b64decode(F_STATE_Former), encoding='utf-8')
    F_STATE_Former_dict = json.loads(F_State_Former_str)
    F_STATE_Former_dict["p1"].update({'Title': p1})
    F_STATE_Former_dict['p1_BaoSRQ'].update({'Text': p1_BaoSRQ})
    F_STATE_Former_dict['p1_TiWen'].update({'Text': p1_TiWen})
    F_STATE_Former_dict['p1_ZaiXiao'].update({'SelectedValue': p1_ZaiXiao})
    F_STATE_Former_dict['p1_ddlXian'].update({'SelectedValueArray': [p1_ddlXian]})
    F_STATE_Former_dict['p1_XiangXDZ'].update({'Text': p1_XiangXDZ})
    F_State_New_str = json.dumps(F_STATE_Former_dict, ensure_ascii=False, separators=(',', ':'))
    F_State_New=base64.b64encode(F_State_New_str.encode("utf-8")).decode()
    return  F_State_New


if __name__ == "__main__":
    studentId = sys.argv[1]
    password = sys.argv[2]
    studentInfoList = [[studentId, password]]
    timeUTC = datetime.datetime.utcnow()
    timeLocal = timeUTC + datetime.timedelta(hours=8)
    date = timeLocal.strftime('%Y - %m - %d')
    if(timeLocal.hour>=19):
        Time_1or2 = "2"
    else:
        Time_1or2 = "1"
    reportData = {"date": date, "temperature": "", "county": "宝山区",
                  "campusLocation": "宝山", "Time_1or2": Time_1or2, "location": "具体地址"}  #county：所在区   cmapusLocation:所在校区

    for studentInfo in studentInfoList:
        reportData.update({'temperature':str(round(random.uniform(36, 36.5), 2))})   #随机温度
        try:
            cookie = get_cookies(studentInfo)
        except:
            print("无法获取学号  " + studentInfo[0] +  "  的cookie,可能是账号密码错误")
            continue
        reportSuccess = daily_report(cookie,reportData)
        if (reportSuccess) == -1 :
            print(str(studentInfo[0] + "   报送失败"))
        else :
            print(str(studentInfo[0] + "   提交成功"))


