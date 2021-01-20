# dailyReport
SHU 每日两报 每日一报

基于request库的自动报送，可部署于服务器实现定时报送
report.py用于进行当日报送
delayReport.py可一次性补报之前日期
# 简介
    该github工程主要是为了解决疫情期间需要不断地申报自身健康而建立,工程中使用GitHub Action来实现每天自动打卡工作。
# 准备工作
    1.一个github账号
    2.一个邮箱账号：用于发送签到成功邮件，推荐添加，为了方便验证是否签到成功（可选）
    一般邮箱都支持以生成验证码的形式进行第三方客户端登陆
#	上手教程

## 1、把代码clone到本地或者直接点击fork按钮将工程复制到你的仓库

![在这里插入图片描述](./IMAGE/fork.png)

## 2、邮件配置

本文以配置88邮箱为例。点击客户端设置，然后生成一个专用密码，将字符串复制，并把它放到第三步里面的MAIL_PASSWORD变量

![在这里插入图片描述](./IMAGE/SMTP.png)
![在这里插入图片描述](./IMAGE/SMTP2.png)

## 3、配置你的账号和密码。
在工程的secrets里面放置你的账号和密码。同样的，如果你不需要发送邮件通知可以不添加邮件配置。（ActonMartin_PASSWORD和ActonMartin_USER两个变量名需要跟epidemic.yml代码里面的一致）

![在这里插入图片描述](./IMAGE/secrets.png)

## 4、修改自己的接收邮箱(如果不想接收邮箱，可以考虑在yml文件中删除下面的代码块)

![在这里插入图片描述](./IMAGE/modify_1.png)

![在这里插入图片描述](./IMAGE/modify_2.png)

![在这里插入图片描述](./IMAGE/modify_3.png)

### 4.1、不想接收邮件的话，删除下面的代码，同时在开始时可以不配置发送邮箱
```
- name: 'Send mail'
          uses: dawidd6/action-send-mail@master
          with:
            server_address: smtp.88.com
            server_port: 465
            username: ${{ secrets.MAIL_USERNAME }}
            password: ${{ secrets.MAIL_PASSWORD }}
            subject: #这个地方是邮件标题# (${{env.REPORT_DATE}})
            body: file://email.txt
            to: chateba@vip.qq.com  #这个地方需要修改
            from: GitHub Actions
            content_type: text/html
```
## 5、修改运行时间

![在这里插入图片描述](./IMAGE/time.png)

```
name: 'epidemic'

on:
  watch:
    types: started
  push:
  schedule:
    - cron: '0 19,21 * * *'
```
19,21加上8小时才是北京时间，所以这个地方设置的是每天北京时间的3点和5点各运行一次。

## 6、创建工作流(如果是fork的可以不用)

![在这里插入图片描述](./IMAGE/workflow.png)

## 7、打开Action查看工作流

![在这里插入图片描述](./IMAGE/workflow2.png)


## 8、上面代码提交之后，会自动运行。同时你也可以点击star运行action


## 9、运行结束后，会有邮件发送

![在这里插入图片描述](./IMAGE/email.png)

## 10、停止运行

之后要是不需要每天填报了，那进入setting-》action-》选择Disable Actions for this repository。该仓库的工作流将不再运行。

![在这里插入图片描述](./IMAGE/stop.png)


参考链接：[GitHub Actions 入门教程](http://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)

[GitHub Actions 教程：定时发送天气邮件](http://www.ruanyifeng.com/blog/2019/12/github_actions.html)

[Python实现自动签到脚本](https://blog.csdn.net/ydydyd00/article/details/80882183)

[手动触发 GitHub Actions 的几种方式](https://p3terx.com/archives/github-actions-manual-trigger.html)

[GitHub Actions 中 python 脚本获取仓库 secrets](https://blog.csdn.net/sculpta/article/details/106474324)

[Selenium2+python自动化46-js解决click失效问题](https://www.cnblogs.com/yoyoketang/p/6569226.html)

[GitHub action fork之后无法触发action](https://github.community/t/forked-repo-doesnt-trigger-action/16259)

[situyun](https://github.com/Saujyun/AutoAction)

