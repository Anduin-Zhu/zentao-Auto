# -*- coding:utf-8 -*-
__author__ = '朱永刚'

import re
import os
import smtplib
from config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from utils.log import logger
from socket import gaierror,error
from utils.config import REPORT_PATH

class Email:

    def __init__(self,  file_path=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        e = Config().get('Email')
        self.title = e.get('title')
        self.message = e.get('message')
        self.files = file_path

        self.msg = MIMEMultipart('related')

        self.server = e.get('server')
        self.sender = e.get('sender')
        self.receiver = e.get('receiver')
        self.password = e.get('password')

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP_SSL(self.server,465)  # 连接sever
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))

"""
class Email:
    '''
    第二种邮件发送方法
    '''
    def sentemail(self,report_file):
        mail_from = '*********@***.com'  # 发件邮箱
        mail_to = '**********@***.com'  # 收件邮箱
        mail_pwd = '**********'  # 授权码
        mail_server = 'smtp.qq.com'  # 发件邮箱服务器
        mail_subject = 'XXX的测试报告'  # 邮件主题
        # 正文
        mail_file = open(report_file, 'rb')
        mail_body = mail_file.read()
        mail_file.close()
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg["Subject"] = Header(mail_subject, 'utf-8')

        mail_smtp = smtplib.SMTP_SSL(mail_server, 465)
        mail_smtp.login(mail_from, mail_pwd)
        mail_smtp.sendmail(mail_from, mail_to, msg.as_string())
        mail_smtp.quit()
        print('email send success!!!')

    def sentreport(self):
        report_dir = REPORT_PATH + r'\\'
        lists = os.listdir(report_dir)
        lists.sort(key=lambda fn: os.path.getmtime(report_dir + fn) if not os.path.isdir(report_dir + fn) else 0)
        print('最新的文件为： ' + lists[-1])
        print('上一次的测试结果：' + lists[-2])
        '''
        指定的邮箱可以正常收到邮件，但所得到的邮件内容是空的，这是由于 HTMLTestRunner 报告文件
        的机制所引起的。在测试用例运行之前生成报告文件，在整个程序没有彻底运行结束前，程序并没有把运
        行的结果写入到文件中，所以，在用例运行完成后发邮件，造成邮件内容是空的。
        所以，我们不能在整个程序未运行结束时发送当前的测试报告，我们可以选择上一次运行结果的报告
        进行发送'''
        file = os.path.join(report_dir, lists[-2])
        # 调用发邮件方法
        self.sentemail(file)
"""