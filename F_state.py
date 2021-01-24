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