# coding:utf8

import requests

import json

import xlwt
import jsonpath
import datetime

''' 
    稳定性测试中批量获取检测结果输出到excle中

    可修改condition中的以下参数值
        name：任务创建人
        checkLanguage：语言项 c/c++:1  Object-C:5 C#:2 Java:0 PHP:4 Python:3 Cobol:6
        addStart/addEnd：取时间差内的任务  如"addStart":"2018-12-01 00:00:00","addEnd":"2018-12-20 00:00:00"
                        获取 2018-12-01 00:00:00 至 2018-12-20 00:00:00 时间段内的任务

     username：用户登录名
     password：密码                 
'''

username = "zhaoyiwei"
passwrod = "ct123!@#"

condit = '{"page":{"pageSize":1000,"pageIndex":1,"checkType":0},"conditions":{"name":"","createPerson":"",' \
            '"checkEngine":null,"checkLanguage":3,"taskStatus":null,' \
            '"source":null,"stime":"","etime":"","minBugCount":"",' \
            '"maxBugCount":"","isFilter":false,' \
            '"addStart":"2019-03-05 00:00:00","addEnd":"2019-03-08 00:00:00",' \
            '"problemNumLB":null,"problemNumRB":null}}'

Rheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

page = '{"page":{"pageSize":15,"pageIndex":1,"checkType":0}}}'


lastpages = {"data": condit}


class Task(object):
    def __init__(self, taskName, problemNum, taskBeginTime, taskEndTime, timeDiff):
        self.taskName = taskName
        self.problemNum = problemNum
        self.taskBeginTime = taskBeginTime
        self.taskEndTime = taskEndTime
        self.timeDiff = timeDiff


def login():
    mdata = {
        'username': username,
        'password': passwrod,
    }
    url = 'https://10.95.14.49/login'
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, params=mdata, headers=Rheaders, verify=False)
    sessionid = response.cookies.get_dict()
    return sessionid


def openUrl(url, param):
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, data=param, headers=Rheaders, verify=False, cookies=login())
    return response.text


def quickCheck():
    quickCheck = 'https://10.95.14.49/quickcheck/list'
    requests.packages.urllib3.disable_warnings()
    print(lastpages)
    response = requests.post(quickCheck, data=lastpages, headers=Rheaders, verify=False, cookies=login())
    return response.text


def parseJson():
    jsonstr = quickCheck()
    print(jsonstr)
    unicodestr = json.loads(jsonstr)
    taskInfo = jsonpath.jsonpath(unicodestr, "$..taskVO")
    taskList = []
    pkTaskList = []
    if not taskInfo:
        print("无数据")
        return
    for i in range(len(taskInfo)):
        timeDiff = getTimeDiff(taskInfo[i]['taskEndTime'], taskInfo[i]['taskBeginTime'])
        if taskInfo[i]['taskStatus'] == 2:
            task = Task(taskInfo[i]['taskName'], taskInfo[i]['problemNum'], taskInfo[i]['taskBeginTime'],
                        taskInfo[i]['taskEndTime'], timeDiff)
        elif taskInfo[i]['taskStatus'] == 3:
            task = Task(taskInfo[i]['taskName'], "检测失败", taskInfo[i]['taskBeginTime'], taskInfo[i]['taskEndTime'],
                        timeDiff)
        taskList.append(task)
        pkTaskList.append(taskInfo[i]['pkTask'])
        print(taskInfo[i])

    CodeLine = getOneTaskInfo(pkTaskList)
    print(CodeLine)
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('稳定性测试', cell_overwrite_ok=True)
    row0 = ["任务名称", "检测结果", "任务开始时间", "任务结束时间", "检测时长", "代码行"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    for i in range(0, len(taskList)):
        sheet1.write(i + 1, 0, taskList[i].taskName)
        sheet1.write(i + 1, 1, taskList[i].problemNum)
        sheet1.write(i + 1, 2, taskList[i].taskBeginTime)
        sheet1.write(i + 1, 3, taskList[i].taskEndTime)
        sheet1.write(i + 1, 4, taskList[i].timeDiff)
        sheet1.write(i + 1, 5, CodeLine[i])
    f.save('test.xls')


def getTimeDiff(taskEndTime, taskBeginTime):
    # print("开始时间"+taskBeginTime+"结束时间"+taskEndTime)
    # ta = time.strptime(taskBeginTime, "%Y-%m-%d %H:%M:%S")
    ta = datetime.datetime.strptime(taskBeginTime, "%Y-%m-%d %H:%M:%S")

    tb = datetime.datetime.strptime(taskEndTime, "%Y-%m-%d %H:%M:%S")
    times = str(tb - ta)  # .split(':')
    difftime = times[0] + '时' + times[1] + '分' + times[2] + '秒'
    # print("时间差"+times)
    return times


nlist = ["xml", "sql", "properties", "sql"]


def getOneTaskInfo(pkTaskList):
    CodeLine = []
    for i in pkTaskList:
        pkTask = '{"pkTask":' + str(i) + ',"isMybug":"N"}'
        params = {"data": pkTask}
        jsonstr = openUrl("https://10.95.14.49/result/queryOneTaskInfo", params)
        unicodestr = json.loads(jsonstr)
        OneTaskInfo = jsonpath.jsonpath(unicodestr, "$..fileTypeAndNum")
        # print(OneTaskInfo[0])
        code = ""
        if len(OneTaskInfo) != 0:
            for i in OneTaskInfo[0]:
                if code + i['key'] not in nlist:
                    code = code + i['key'] + ":" + i['value']
        else:
            code = "无缺陷"
        CodeLine.append(code)

    return CodeLine


parseJson()
# quickCheck()





