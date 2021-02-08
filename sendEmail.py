# 发送纯文本的邮件
# 发送html页面的邮件
# 发送带附件文件的邮件
# 发送能展示图片的邮件
# 参考： https://zhuanlan.zhihu.com/p/89868804
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage  # 负责构造图片
from email.mime.multipart import MIMEMultipart  # 负责将多个对象集合起来
from email.mime.text import MIMEText  # 负责构造文本
from email.header import Header

class email(object):
    """封装发送邮件类"""

    def __init__(self, mail_host, mail_sender, mail_license, mail_receivers, subject_content="""Python邮件测试""",
                 port=25):

        self.mail_sender = mail_sender
        self.mail_receivers = mail_receivers

        # 创建SMTP对象
        self.stp = smtplib.SMTP()
        # 设置发件人邮箱的域名和端口，端口地址为25
        self.stp.connect(mail_host, port=port)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        self.stp.login(mail_sender, mail_license)

        # 1 构建MIMEMultipart对象代表邮件本身，可以往里面添加文本、图片、附件等
        self.msg = MIMEMultipart('related')

        # 2 设置邮件头部内容
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        self.msg["From"] = mail_sender
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        self.msg["To"] = mail_receivers
        # 设置邮件主题
        self.msg["Subject"] = Header(subject_content, 'utf-8')

    def addBody(self, body_content="你好，这是一个测试邮件", content_type='plain'):
        # 3 邮件正文内容
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, "plain", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        self.msg.attach(message_text)

    def addFile(self, filePath):
        # 构造附件
        atta = MIMEText(open(filePath, 'rb').read(), 'base64', 'utf-8')
        # 设置附件信息
        atta['Content-Type'] = 'application/octet-stream'
        atta["Content-Disposition"] = 'attachment; filename="attach.txt"'
        # 添加附件到邮件信息当中去
        self.msg.attach(atta)

    def addImage(self, imagePath):
        # 二进制读取图片
        image_data = open(imagePath, 'rb')
        # 设置读取获取的二进制数据
        message_image = MIMEImage(image_data.read())
        # 关闭刚才打开的文件
        image_data.close()
        # 添加图片文件到邮件信息当中去
        self.msg.attach(message_image)

    def send(self):
        # 4 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        self.stp.sendmail(self.mail_sender,
                              self.mail_receivers, self.msg.as_string())
        # 关闭SMTP对象
        self.stp.quit()
        print("邮件发送成功")


