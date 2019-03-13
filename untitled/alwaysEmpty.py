from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from pykeyboard import PyKeyboard
from selenium.webdriver.support.ui import WebDriverWait
from pymouse import PyMouse
import pyautogui
import threading
import time


#chrome_options = Options()
#chrome_options.add_argument('--headless')
#browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Firefox()

#options = webdriver.FirefoxOptions()
#options.add_argument('-headless')
#browser = webdriver.Firefox(options=options)
browser.get("https://10.95.14.49")
browser.implicitly_wait(10)


def openBrowser():
    browser.find_element_by_xpath("//*[@placeholder='请输入用户名']").send_keys('zhaoyiwei')
    # browser.find_element_by_id('username').send_keys('zhaoyiwei')
    # browser.find_element_by_id('password').send_keys('ct123!@#')
    browser.find_element_by_xpath("//*[@placeholder='请输入密码']").send_keys('ct123!@#')
    browser.find_element_by_tag_name('button').click()


def newRisk(filename, path='G:\\zhaoyiwei\\OpenSourceProjectSample\\completed'):
    browser.implicitly_wait(10)
    # 当控件未加载完成，等待10s
    browser.find_element_by_css_selector("[class='txt ng-binding']").find_element_by_xpath(
        "//span[text()='快速检测']").click()
    # 快速检测
    browser.find_element_by_css_selector("[class='btn btn-green']").click()
    # 发起快速检测
    browser.find_element_by_name('taskname').send_keys(filename)
    # 填写任务名称
    browser.find_element_by_xpath("//input[@value='0']").click()
    '''选择语言：修改对应value值
    c/c++:1  Object-C:5 C#:2 Java:0 PHP:4 Python:3 Cobol:6
    '''
    sleep(3)
    #upload = browser.find_element_by_id('fileUpload')
    #print(upload.get_attribute('style'))
    '''js = "var q=document.getElementById(\"fileUpload\");q.style=\"display: block;\";"
    browser.execute_script(js)
    browser.find_element_by_id('fileUpload').send_keys(path + '\\' + filename + '.zip')
    print(browser.find_element_by_id('fileUpload').get_attribute('value'))
    alert = browser.switch_to.alert
    print(alert.text)'''
    browser.find_element_by_class_name('btn-default').click()
    sleep(1)
    k = PyKeyboard()
    # k.tap_key(k.esc_key)
    #k.tap_key(k.tab_key, n=3)
    #k.press_key(k.enter_key)
    sleep(1)
    alert = browser.switch_to.window('文件上传')
    print(alert.text)
    #browser.find_element_by_id('fileUpload').send_keys(path + '\\' + filename + '.zip')
    #re_exe()
    # browser.execute_script("window.close()")
    #button = browser.find_element_by_class_name('btn-green')
    #is_visible = WebDriverWait(browser).until(lambda driver: button.is_displayed())
    #print(is_visible)
    #button.click()
    #sleep(300)
    #browser.find_element_by_class_name('btn-green').click()


def newRisks():
    openBrowser()
    rootdir = 'G:\\zhaoyiwei\\OpenSourceProjectSample\\completed'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, 1):
        path = os.path.join(rootdir, list[i])
        filename = path[:-4]
        if os.path.isfile(path):
            print(os.path.basename(filename))
            newRisk(os.path.basename(filename))
    #browser.quit()

def re_exe():
    while True:
        isDis = browser.find_element_by_class_name('btn-green').is_displayed()
        #print(isDis)
        if not isDis:
            time.sleep(5)
        else:
            browser.find_element_by_class_name('btn-green').click()
            break


newRisks()
# openBrowser()


