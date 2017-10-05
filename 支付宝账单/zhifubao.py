import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


login_url='https://auth.alipay.com/login/index.htm'                  #登录支付宝地址
info_url='https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauth.alipay.com%2Flogin%2Findex.htm'     #跳转到登录成功后的地址


Username='15659819902'         #登录用户账号
Password='wojiaozy'         #登录用户密码


Headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'Referer': 'https://authem14.alipay.com/login/loginResultDispatch.htm ',
    'Host': 'my.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}
    ##设置session管理器的headers

'''
get_cookie='cna=XY5OEqxplVYCAbf61VfxMHJV; session.cookieNameId=ALIPAYJSESSIONID; unicard1.vm="K1iSL1gmCrk3R46G9RJAjg=="; ALIPAYJSESSIONID.sig=VldDHWwkb1LpoHpzj5Xom5ztC-X79qWvCfuS53M40W8; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; ctoken=ZOccqu7dG8xDvfcJ; LoginForm=alipay_login_auth; alipay="K1iSL1gmCrk3R46G9RJAjvqB44VlrCkWZzN1IpWMcw=="; CLUB_ALIPAY_COM=2088112106518890; iw.userid="K1iSL1gmCrk3R46G9RJAjg=="; ali_apache_tracktmp="uid=2088112106518890"; zone=RZ24B; _hvn_login=1; CHAIR_SESS=K6iO619fGWnMOmQO_wFsrP4bQsKn15nE2eMjJpHif8HLoxJ6QfIBhrtrrlyZBwF9m_Zge8Aar7kkkzJ4bZvZRiXeTTi4SoZA0qQAe7D0FpLNhxCttMbcCgZsx09vwmZWZTEhPKfrQRDLIgtPZpc3mQ==; spanner=jsu2idChsDJCMIPMOKpRNUucecgk4T7sXt2T4qEYgj0=; ALIPAYJSESSIONID=RZ24PR5MIx3fJdx7XhTNEy6bQmc99kauthRZ24GZ00; rtk=tN8oxx0XSsW/jTKohNH8x0sbFsXQehrXPHavLXT2BQIozGi8L7o'
cookie=SimpleCookie(get_cookie)
cookies={i.key:i.value for i in cookie.values()}
'''


class Aliplay_info(object):
    def __init__(self,headers,username,password):
        self.headers=headers
        self.username=username
        self.password=password
        self.session=requests.Session()
        self.session.headers=self.headers           #设置Session 的headers
        #self.cookie=cookie
        #self.session.cookies.update(self.cookies)
        self.info_list=[]

    def wait_input(self,ele,str):           #模拟输入用户账号和密码，这里因为支付宝的认证机制，所以需要设定延迟输入字符
        for i in str:
            ele.send_keys(i)
            time.sleep(0.5)


    def get_cookie(self):
        dacp=dict(DesiredCapabilities.PHANTOMJS)    ###这两句是为PhantomJS浏览器设置headers，如果没有模拟浏览器的headers会被当作爬虫禁止访问
        dacp["phantomjs.page.settings.userAgent"]=("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36")
        sel=webdriver.PhantomJS(desired_capabilities=dacp)
        sel.maximize_window()  #最大窗口化
        sel.get(login_url)     #进入支付宝登录界面
        sel.implicitly_wait(3)

        usname=sel.find_element_by_id('J-input-user')       #找到输入账号窗口
        usname.clear()                                         #输入之前清除输入框，保证输入框没有任何字符
        print('正在输入账号')
        self.wait_input(usname,self.username)               #延迟输入账号
        uasswd=sel.find_element_by_id('password_rsainput')          #找到密码输入框
        uasswd.clear()                                          #输入之前清除输入框，保证输入框没有任何字符
        print('正在输入密码')
        self.wait_input(uasswd,self.password)                  #延迟输入密码

        button=sel.find_element_by_id('J-login-btn')            #找到登录按钮
        time.sleep(1)
        button.click()                                             #延迟点击登录

        print(sel.current_url)                                      #打印当前的url
        curr_url=sel.current_url
        print('正在跳转》》》》')

        ll=sel.get(info_url)                                           #登录成功后跳转到我的支付宝界面
        print(ll)
        sel.implicitly_wait(3)
        cookies=sel.get_cookies()                                      #找到当前页面的cookies
        print(cookies)
        cookie_dict={}
        for cookie in cookies:
            if 'name'in cookie and'value'in cookie:                 #找到cookies中有用的name和value信息
                cookie_dict[cookie['name']]=cookie['value']
        print(cookie_dict)
        sel.close()             #关闭浏览器
        return cookie_dict


    def sset_cok(self):

        sck=self.get_cookie()
        self.session.cookies.update(sck)            #对session中的cookie进行更新
        #print(self.session.cookies)





    def login_stasus(self):
        self.sset_cok()
        status=self.session.get(info_url, timeout=5, allow_redirects=False).status_code  #session访问我的支付宝界面，重定向关闭
        print(status)
        if status==200:
            return True
        else:
            return False
    def get_data(self):
        status=self.login_stasus()
        print(status)
        if status:                                          #假如返回200 ok说明访问成功
            html=self.session.get(info_url).text
            print(html)
            soup=BeautifulSoup(html,'lxml')
            #print(soup)
            info1_list=soup.find_all('tr',class_='J-item')[:5]
            trades = soup.find_all('table', class_='ui-record-table table-index-bill')
            print(trades)
            info2_list=soup.find_all('tr',class_='J-item split  ')[:5]
            '''
            抓取交易前5条的记录，包含时间、交易详情、交易金额、交易流水号
            '''
            for info in info1_list:
                try:
                    time=info.find('p',class_='time-d').text.strip()
                    content=info.find('p',class_='consume-title').a.text.strip()
                    money=info.find('span',class_='amount-pay').text.strip()
                    id=info.find('select',class_='fn-hide J-operation-select').option['data-link']
                    self.info_list.append(dict(time=time,content=content,money=money,id=id))
                except:
                    self.info_list.append('出错啦~~~')
            for info1 in info2_list:
                try:
                    time=info1.find('p',class_='time-d').text.strip()
                    content=info1.find('p',class_='consume-title').a.text.strip()
                    money=info1.find('span',class_='amount-pay').text.strip()
                    id=info1.find('select',class_='fn-hide J-operation-select').option['data-link']
                    self.info_list.append(dict(time=time,content=content,money=money,id=id))
                except:
                    self.info_list.append('出错啦~~~')
        else:
            self.info_list.append('不好意思，断开啦~')
        return self.info_list
test=Aliplay_info(Headers,Username,Password)
data = test.login_stasus()
print(data)