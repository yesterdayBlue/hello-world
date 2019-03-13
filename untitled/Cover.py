#coding=utf-8

#通过minidom解析xml文件
import xml.dom.minidom as xmldom
import os
import xlwt
import requests
import jsonpath
import json
class Ele(object):
    def __init__(self, subClass, obsolete):
        self.subClass = subClass
        self.obsolete = obsolete

def parsXML(path):
    allEle=[]
    xmlfilepath = os.path.abspath(path)
    # 得到文档对象
    domobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    elementobj = domobj.documentElement
    # 获得子标签
    subElementObj = elementobj.getElementsByTagName("Categories")
    subElementObj1 = elementobj.getElementsByTagName("Obsolete")

    i = 0
    for ca in subElementObj:
        ele = Ele(ca.getElementsByTagName('Category')[2].childNodes[0].data,subElementObj1[i].firstChild.data)
        allEle.append(ele)
        i=i+1
    return allEle

def toExcel(allEle,bugEle):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('冒烟测试', cell_overwrite_ok=True)
    row0 = ["应检出缺陷", "实际检出缺陷","备注"]
    # 写第一行
    mid = []
    for i in range(0, len(allEle)):
        mid.append(allEle[i].subClass)
    print(mid)
    print(bugEle)
    for i in range(0, len(mid)):
        if mid[i] not in bugEle:
           index = mid.index(mid[i])
           mid[index] = ""
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    for i in range(0, len(allEle)):
        sheet1.write(i + 1, 0, allEle[i].subClass)
        sheet1.write(i + 1, 2, "已废弃" if (allEle[i].obsolete=="yes") else "")
        sheet1.write(i + 1, 1, mid[i])

    f.save('maoyan.xls')

def parseJson(pkTask,username,password):
    Rheaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    mdata = {
        'username': username,
        'password': password,
    }
    para = '{"pkTask":'+pkTask+',"treeType":"A","isMybug":"N","isBugTypeList":"T"}'
    AllBugs ={"data":para}
    url = 'https://10.95.14.49/login'
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, params=mdata, headers=Rheaders, verify=False)
    sessionid = response.cookies.get_dict()
    quickCheck = 'https://10.95.14.49/result/queryAllBugsType'
    response = requests.post(quickCheck, data=AllBugs, headers=Rheaders, verify=False, cookies=sessionid)
    jsonstr = response.text
    unicodestr = json.loads(jsonstr)
    bugtype = jsonpath.jsonpath(unicodestr, "$..sons")
    realList = []
    for i in range(len(bugtype)):
        for j in range(len(bugtype[i])):
            if 0 != len(bugtype[i][j]):
                realList.append(bugtype[i][j]["typeName"])
    return realList

'''
    覆盖性测试获取对比结果
    toExcel(parsXML(path),parseJson(pkTask))
        path：知识库路径 如：E:\\zhaoyiwei\\测试机知识库\\java_buginfos_bug.xml 注：路径分隔符需为'\\’
        pkTask：任务号 如：覆盖性测试结果url为：https://10.95.14.49/#/audit/1416/0 其中去1416为任务号
'''
toExcel(parsXML("E:\\zhaoyiwei\\测试机知识库\\java_buginfos_bug.xml"),parseJson('1416','zhaoyiwei','ct123!@#'))

