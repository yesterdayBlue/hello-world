# -*- coding:utf-8 -*-

import requests
import os
import urllib.request
from pyquery import PyQuery
from urllib.request import urlopen

def GetGitHubURL(urllist, namelist):
    for page in range(1, 2):
        #url = "https://github.com/search?p=".format(page) + "&q=size%3A%3E500000+language%3Ajava&type=Repositories"
        url = "https://github.com/search?p=2&q=ibatis&type=Repositories"
        # url = "https://github.com/search?utf8=%E2%9C%93&q=java"
        # url = "https://github.com/trending/python"
        r = requests.get(url)
        for i in PyQuery(r.content)(".repo-list>li"):
            repo_url = "https://github.com" + PyQuery(i).find(".pr-md-3 a").attr("href") + '/archive/master.zip'
            index = PyQuery(i).find(".pr-md-3 h3 a").text().index("/")
            name = PyQuery(i).find(".pr-md-3 h3 a").text()[index + 1:].strip()
            urllist.append(repo_url)
            namelist.append(name)
            print("项目：" + name, "项目地址：" + repo_url)


def downloadZip(urllist, namelist):
    count = 0
    dir =  'D:/Program Files/PythonWorkSpace/ct/java/mybatis/'
    for item in urllist:
        if os.path.exists(os.path.join(dir, namelist[count] + '.zip')):
            count = count + 1
        else:
            try:
                '''print('正在下载' + namelist[count])
                work_path = os.path.join(dir, namelist[count] + '.zip')
                urllib.request.urlretrieve(item, work_path)
                count = count + 1'''
                response = urlopen(item)
                chunk = 16 * 1024
                with open(dir+namelist[count]+'.zip', 'wb') as f:
                    while True:
                        chunk = response.read(chunk)
                        if not chunk:
                            break
                        f.write(chunk)
            except:
                    continue


def main():
    urllist = []
    namelist = []
    GetGitHubURL(urllist, namelist)
    #downloadZip(urllist, namelist)


main()

