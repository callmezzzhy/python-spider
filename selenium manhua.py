from selenium import webdriver
import os
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
'''
为PhantomJs浏览器设置User-Agent
'''
da=dict(DesiredCapabilities.PHANTOMJS)
da["phanjomjs.page.settings.userAgent"]=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
'''
创建目录
'''
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
def savepicture(filname,url):
    content=requests.get(url).content
    with open(filname,'wb')as f:
        f.write(content)
def get_url(index_url):
    url_list=[]
    brower=webdriver.Chrome('D:\\firefox\\chromedriver.exe')
    brower.get(index_url)
    brower.implicitly_wait(3)
    title=brower.title.split(',')[0]
    mkdir(title)
    commic_list=brower.find_elements_by_class_name('comic_Serial_list')
    for commic in commic_list:
        links = commic.find_elements_by_tag_name('a')
        # 找到每个单独的章节链接
        for link in links:
            url_list.append(link.get_attribute('href'))
    brower.quit()
    comics=dict(titles=title,url=url_list)
    print(comics)
    return comics

def get_picture(commics):
    comiclist=commics['url']
    dirname=commics['titles']
    brower=webdriver.Chrome('D:\\firefox\\chromedriver.exe')
    for urls in comiclist:
        #brower=webdriver.PhantomJS(desired_capabilities=da)
        brower.get(urls)
        brower.implicitly_wait(3)
        dirnames=dirname+'/'+''.join(brower.title.split('-')[0]+brower.title.split('-')[1]).replace('.','')
        mkdir(dirnames)
        pages=brower.find_elements_by_tag_name('option')
        next_page=brower.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        for i in range(len(pages)):
            '''
            #xpath 一级一级找到img节点，获取src属性值，即漫画图片地址
            ''''
            page_url=brower.find_element_by_xpath('/html/body/table/tbody/tr/td/a/img').get_attribute('src') 
            #fil=brower.find_element_by_xpath('/html/body/div[@class="wrap"]/span[1]/').text
            print(page_url)
            filename=dirnames+'/'+str(i)+'.png'
            savepicture(filename,page_url)
            next_page.click()
        print('当前章节\t{}  下载完毕'.format(brower.title))
    brower.quit()
    print('下载完毕')
def main():
    url=input('请输入漫画地址')
    comic=get_url(url)
    get_picture(comic)

if __name__=='__main__':
    main()
