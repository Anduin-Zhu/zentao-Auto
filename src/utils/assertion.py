# -*- coding:utf-8 -*-
__author__ = '朱永刚'

"""
可以添加各种自定义断言，断言失败时抛出AssertionError就行
"""

def assertHTTPCode(response,code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        raise AssertionError('相应code不在列表中') # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error

def assertText(locator,text_list=None):
    loc_text = locator.text
    if not text_list:
        text_list = ['欢迎来到运营']
    if loc_text not in text_list:
        raise  AssertionError('登录失败')

