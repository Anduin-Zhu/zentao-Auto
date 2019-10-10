# -*- coding:utf-8 -*-
__author__ = '朱永刚'

import time
import os
from selenium import webdriver
from utils.config import DRIVER_PATH,REPORT_PATH

#可以根据需要自行扩展
FIREFOX_PATH = os.path.join(DRIVER_PATH,'geckodriver')
IEDRIVER_PATH = os.path.join(DRIVER_PATH,'IEDriverServer')
CHROMEDRIVER_PATH = os.path.join(DRIVER_PATH,'chromedriver')

TYPES = {'firefox':webdriver.Firefox,'ie':webdriver.Ie,'chrome':webdriver.Chrome}

EXECUTABLE_PATH = {'firefox':FIREFOX_PATH,'ie':IEDRIVER_PATH,'chrome':CHROMEDRIVER_PATH}

class UnSupportBrowserTypeError(Exception):
    pass

class Browser(object):
    """可以根据传入的参数选择浏览器的driver打开对应浏览器，并且增加一个保存截图的方法，将截图保存到report目录下"""
    def __init__(self,browser_type=None):
        self._type = browser_type.lower()#lower()方法：将大写字符转换成小写
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            raise UnSupportBrowserTypeError('仅支持%s！'%','.join(TYPES.keys()))
        self.driver = None

    def get(self,url,maxmize_windows=True,implicitly_wait=30):
        self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
        self.driver.get(url)
        if maxmize_windows:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self

    def save_screen_shot(self,name='screen_shot'):
        day = time.strftime('%Y%m%d',time.localtime(time.time()))
        screenshot_path = REPORT_PATH + r'\screenshot_%s' %day
        if not os.path.exists(screenshot_path):
            #递归创建目录
            os.makedirs(screenshot_path)

        tm = time.strftime('%H%M%S',time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + r'\\%s_%s.png'%(name,tm))
        return screenshot

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    b = Browser('chrome').get('https://www.baidu.com')
    b.save_screen_shot('test_baidu')
    time.sleep(3)
    b.quit()