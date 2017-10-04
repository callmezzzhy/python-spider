from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
def post(data):
    host_server='smtp.qq.com' 
    sender_qq='xxxxxxx                           #发送方qq号
    pwd='xxxxxx'                       #qq开启第三方smtp 验证码
    sender_qq_mail='xxxxxxx@qq.com'              #发送方邮箱
    receiver ='xxxxxxx@qq.com' #接收者邮箱
    mail_content=('你好，你查询的车票信息：{} 有票啦，可以赶紧登陆抢票 '.format(data))           #邮件内容
    mail_title='来自远方的一封信'                   #邮件标题
    smtp=SMTP_SSL(host_server)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq,pwd)
    '''
    配置邮件内容及格式
    '''
    msg=MIMEText(mail_content,"html",'utf-8')
    msg["Subject"]=Header(mail_title,'utf-8')
    msg["From"]=sender_qq_mail
    msg["To"]=receiver
    smtp.sendmail(sender_qq_mail,receiver,msg.as_string())  
    smtp.quit()


