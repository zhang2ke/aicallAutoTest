import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.configInfo import ConfigInfo
from common.log import Logger


class SendEmail(object):
    def __init__(self, msg_body, appendix):
        self.mail_info = ConfigInfo().get_email_info()
        self.mail_switch = self.mail_info["email_switch"]
        self.host = self.mail_info["host"]  # smtp服务器地址
        self.sender = self.mail_info["sender"]  # 发送邮箱
        self.pwd = self.mail_info["pwd"]  # 发送邮箱密码
        self.receivers = self.mail_info["receivers"]
        self.subject = self.mail_info["subject"]  # 邮件标题
        self.content = msg_body  # 邮件正文
        if isinstance(appendix, str):  # 附件路径
            self.appendix = []
            self.appendix.append(appendix)
        else :
            self.appendix = appendix

        self.port = 25  # 普通端口
        self.ssl = True  # 是否安全链接
        self.ssl_port = 465  # 安全链接端口

        self.logger = Logger().get_logger()

        if self.mail_switch == "on":
            self.send_email()
        else :
            self.logger.info("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")

    def send_email(self):
        msg = MIMEMultipart()  # 发送内容的对象
        msg['Subject'] = self.subject  # 邮件主题
        msg['From'] = self.sender
        msg['To'] = ','.join(self.receivers)  # 接收者
        msg.attach(MIMEText(self.content, _subtype='html', _charset='utf-8'))  # 邮件正文的内容

        if self.appendix is None:
            self.logger.info("附件列表为空")
        else:
            for append in self.appendix:
                if os.path.exists(append):  # 处理附件
                    attach_name = os.path.split(append)[-1]  # 只取文件名，不取路径
                    try:
                        attach = MIMEApplication(open(append, 'rb').read())
                        attach.add_header('Content-Disposition', 'attachment', filename=attach_name)
                        msg.attach(attach)
                    except Exception as e:
                        self.logger.info("Error: 添加附件%s出现异常，异常信息:%s" % (append, e))
                else:
                    self.logger.info("Error: 附件%s不存在" % append)

        server = smtplib.SMTP_SSL(self.host, port=self.ssl_port) if self.ssl else smtplib.SMTP(self.host, port=self.port)
        server.login(self.sender, self.pwd)  # 发送邮件服务器的对象
        try:
            server.sendmail(self.sender, self.receivers, msg.as_string())
            self.logger.info('测试报告发送成功')
        except Exception as e:
            self.logger.info('Error: 测试报告发送失败, %s' % e)
        server.quit()


if __name__ == '__main__':
    file = [r"E:\pythtonProject\interfaceTest\result\test.html"]
    # content = "测试发送邮件"
    with open(file[0], "rb") as f:
        content = f.read()
        f.close()
    print(content)
    SendEmail(content, file)
