from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
def post():
    host_server='smtp.qq.com'
    sender_qq='470340062'
    pwd='pyzuyfoqlxrgcbdi'
    sender_qq_mail='470340062@qq.com'
    receiver ='657984297@qq.com'
    mail_content='你好，我是来自知乎的callmezzzhy，现在在进行一项用python登录qq邮箱的练习'
    mail_title='来自远方的一封信'
    smtp=SMTP_SSL(host_server)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq,pwd)
    msg=MIMEText(mail_content,"html",'utf-8')
    msg["Subject"]=Header(mail_title,'utf-8')
    msg["From"]=sender_qq_mail
    msg["To"]=receiver
    smtp.sendmail(sender_qq_mail,receiver,msg.as_string())
    smtp.quit()


