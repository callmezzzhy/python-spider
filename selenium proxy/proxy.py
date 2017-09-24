from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
class Item(object):
    ip=None
    port=None
    anoymous=None
    type=None
    local=None
    speed=None
    time=None
class Gateproxy(object):
    def __init__(self):
        self.starturl='http://www.kuaidaili.com/free/inha/'
        self.urls=self.get_url()
        self.proxy_list=self.getproxy(self.urls)
        self.filename = 'proxy.txt'
        self.savelist=self.save_list(self.filename,self.proxy_list)

    def get_url(self):
        urls=[]
        for i in range(1,4):
            url=self.starturl+str(i)
            urls.append(url)
        return urls
    def getproxy(self,urls):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        proxylists=[]

        for url in urls:
            browser.get(url)
            browser.implicitly_wait(3)
            elements=browser.find_elements_by_xpath('//tbody/tr')
            for element in elements:
                item=Item()
                item.ip=element.find_element_by_xpath('./td[1]').text
                item.port=element.find_element_by_xpath('./td[2]').text
                item.anonymous = element.find_element_by_xpath('./td[3]').text
                item.type=element.find_element_by_xpath('./td[4]').text
                item.local = element.find_element_by_xpath('./td[5]').text
                item.speed = element.find_element_by_xpath('./td[6]').text
                item.time=element.find_element_by_xpath('./td[7]').text
                print(item.ip)
                proxylists.append(item)
        browser.quit()
        return proxylists
    def save_list(self,filename,proxys):
        with open(filename,'a+',encoding='utf-8')as f:
            f.write('免费代理：\tip：\t端口：\t匿名：\t代理：\t位置：\t验证时间：\t\n')
            for proxy in proxys:
                f.write('{}\t{}\t{}\t{}\t{}\t{}\t\n'.format(proxy.ip,proxy.port,proxy.anoymous,proxy.local,proxy.speed,proxy.time))
if __name__=='__main__':
    get=Gateproxy()



