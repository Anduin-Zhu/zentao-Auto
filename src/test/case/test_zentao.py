# -*- coding:utf-8 -*-
__author__ = '朱永刚'

import os
import time
import unittest
from utils.config import Config,DATA_PATH,REPORT_PATH
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.mail import Email
from test.page.zentao_my_page import ZenTaoLoginPage,ZenTaoMyPage

class TestZenTao(unittest.TestCase):
    URL = Config().get('URL')
    excel = os.path.join(DATA_PATH,'data.xlsx')

    def sub_setUp(self):
        #初始页面是main page，传入浏览器类型打开浏览器
        self.page = ZenTaoLoginPage(browser_type='chrome').get(self.URL,maxmize_windows=True)

    def sub_tearDown(self):
        self.page.quit()

    def test_login(self):
        #可以对用例简单说明
        u"""用户登录"""
        datas = ExcelReader(self.excel,title_line=True).data
        for d in datas:# {username:XXX，passwd:123456}
            with self.subTest(data=d):
                self.sub_setUp()
                self.page.login(d['LoginName'],d['PassWd'])
                time.sleep(2)# 等待两秒截图的时间
                self.page.save_screen_shot('test_login')# 调用截图方法
                self.page = ZenTaoMyPage(self.page)# 页面跳转到My_page
                locator = self.page.login_result
                for loc in locator:
                    self.assertEqual(loc.text,'我的地盘',msg='登录失败')
                self.sub_tearDown()


        pass

if __name__ == '__main__':#Alt + Shift +F10 以文件模式执行会出报告
    #unittest.main(verbosity=2)
    # 报告格式
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report = REPORT_PATH + r'\\' + now + 'report.html'
    f = open(report, 'wb')
    runner = HTMLTestRunner(f, verbosity=2, title=u'禅道测试报告', description=u'用例执行情况')
    runner.run(TestZenTao('test_login'))
    #第一种邮件发送方法
    """
    e = Email(title='百度测试报告',
              message='这是今天的测试报告，请查收。',
              server='smtp.qq.com',
              sender='************@qq.com',
              password='授权码',
              receiver='********@qq.com',
              path=report)"""
    e = Email(file_path=report)
    #e.send()

    #Email().sentreport()#这是第二种发送邮件方法