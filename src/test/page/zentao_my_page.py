# -*- coding:utf-8 -*-
__author__ = '朱永刚'

from selenium.webdriver.common.by import By
from test.page.zentao_login_page import ZenTaoLoginPage
from test.common.page import Page

class ZenTaoMyPage(Page):
    loc_login_result = (By.CSS_SELECTOR, 'a.active > span:nth-child(1)')


    @property
    def login_result(self):
        return self.find_elements(*self.loc_login_result)

