# -*- coding:utf-8 -*-
__author__ = '朱永刚'

from selenium.webdriver.common.by import By
from test.common.page import Page
from selenium import webdriver

class ZenTaoLoginPage(Page):
    locator_userName = (By.CSS_SELECTOR,'#account')
    locator_passWord = (By.NAME,'password')
    locator_keepLoginon = (By.ID,'keepLoginon')
    locator_submit = (By.ID,'submit')
    def login(self,userNmae,passWord):
        """登录并保持登录"""
        self.find_element(*self.locator_userName).send_keys(userNmae)
        self.find_element(*self.locator_passWord).send_keys(passWord)
        self.find_element(*self.locator_keepLoginon).click()# 保持登录
        self.find_element(*self.locator_submit).click()

if __name__ == '__main__':
    url = 'http://127.0.0.1/zentao/user-login.html'
    driver = webdriver.Chrome(executable_path=r'D:\Users\dell\PycharmProjects\zentao-Auto\drivers\chromedriver.exe')
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_id('account').send_keys('admin')
    driver.find_element_by_name('password').send_keys('Password@123')
    driver.find_element_by_id('keepLoginon').click()
    driver.find_element_by_id('submit').click()