import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)

def savepic(filename,url):

	content=requests.get(url).content
	with open(filename,'wb')as f:
		f.write(content)
def get_tof(index_url):
	url_list=[]
	browser=webdriver.Chrome('D:\\firefox\\chromedriver.exe')
	browser.get(index_url)
	browser.implicitly_wait(3)
	title=browser.title.split(',')[0]
	mkdir(title)
	comic_lists=browser.find_elements_by_class_name('comic_Serial_list')
	for path in comic_lists:
		links=path.find_elements_by_tag_name('a')
		for link in links :
			url_list.append(link.get_attribute('href')) 
	browser.quit()
	Comics=dict(name=title,urls=url_list)
	return Comics


def get_pic(Comics):
	comic_list=Comics['urls']
	basedir=Comics['name']
	browser=webdriver.Chrome('D:\\firefox\\chromedriver.exe')
	for url in comic_list:
		browser.get(url)
		browser.implicitly_wait(3)


		dirname=basedir+'/'+browser.title.split('-')[0]+browser.title.split('-')[1]
		mkdir(dirname)


		pagenum=len(browser.find_elements_by_tag_name('option'))
		
		nextpage=browser.find_element_by_xpath('//div[@class="page_turning"]/a[4]')
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
		