# -*- coding:utf-8 -*-

class Task(object):
    def __init__(self, taskName, problemNum):
        self.taskName = taskName
        self.problemNum = problemNum

    # def getTaskName(self):
    #     return self.__taskName
    #
    # def setTaskName(self, taskName):
    #     self.__taskName = taskName
    #
    # def getProblemNum(self):
    #     return self.__problemNum
    #
    # def setProblemNum(self, problemNum):
    #     self.__problemNum = problemNum
task = Task("1","2")
print(task)