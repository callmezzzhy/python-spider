import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
'''
创建目录
'''
def mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)
'''
保存图片
'''
def savepic(filename,url):

	content=requests.get(url).content
	with open(filename,'wb')as f:
		f.write(content)
def get_tof(index_url):
	url_list=[]
	browser=webdriver.Chrome('D:\\firefox\\chromedriver.exe')  #打开谷歌刘喇叭钱
	browser.get(index_url)
	browser.implicitly_wait(3)
	title=browser.title.split(',')[0]
	mkdir(title)
	comic_lists=browser.find_elements_by_class_name('comic_Serial_list')  #找到漫画所有章节节点
	for path in comic_lists:
		links=path.find_elements_by_tag_name('a')
		for link in links :
			url_list.append(link.get_attribute('href'))    #所有章节的链接地址
	browser.quit()    #关闭浏览器
	Comics=dict(name=title,urls=url_list)  #建字典
	return Comics


def get_pic(Comics):
	comic_list=Comics['urls']
	basedir=Comics['name']
	browser=webdriver.Chrome('D:\\firefox\\chromedriver.exe') #打开模拟浏览器
	for url in comic_list:
		browser.get(url)
		browser.implicitly_wait(3)   #智能等待响应时间


		dirname=basedir+'/'+browser.title.split('-')[0]+browser.title.split('-')[1]
		mkdir(dirname)


		pagenum=len(browser.find_elements_by_tag_name('option'))  #每章漫画的页数
		
		nextpage=browser.find_element_by_xpath('//div[@class="page_turning"]/a[4]')  #下一页的按钮id
		for i in range(pagenum) :
			pic_url=browser.find_element_by_id('curPic').get_attribute('src')
			filename=dirname+'/'+str(i)+'.png'
			savepic(filename,pic_url)
			nextpage.click()

		print('当前章节\t{}  下载完毕'.format(browser.title))

	browser.quit()
	print('所有章节下载完毕')

def main():
	ur="http://manhua.sfacg.com/mh/WSDJS/"
	#url=str(input('请输入漫画首页地址： \n'))
	Comics=get_tof(ur)
	get_pic(Comics)

if __name__ == '__main__':
	main()
		
