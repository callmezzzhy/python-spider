import requests
from bs4 import BeautifulSoup
import os
def get_html(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding='gbk'
        return r.text
    except:
        return 'error'
'''
创建目录文件
'''

def mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)
''''
保存图片

'''
def savepic(filename,url):
    pic=requests.get(url).content
    with open(filename,'wb')as f:
        f.write(pic)
def get_content(url):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    info=soup.find('ul',class_='picList clearfix')
    movie=info.find_all('li')      #每条排行榜上的电影信息都包含在li节点里

    for li in movie:
        imag_url='http:'+li.find('img')['src']       #找到电影海报图片地址
        title=li.find('a',class_='aPlayBtn')['title'].strip()	#找到电影名
        links='http:'+li.find('a',class_='aPlayBtn')['href']	#找到电影链接地址
        try:
            time = li.find('span',class_='sIntro').text		#找到电影上映时间
        except:
            time = "暂无上映时间"
        try:
            actor=li.find('p',class_='pActor').contents         #找到电影主演名
        #print(actor)
	    actors=''
            for act in actor:
                actors = '' + act.string +'  '
        except :
            actors='无'
        txx=li.find('p',class_='pTxt pIntroShow').text.strip()   #找到电影内容简介
        '''
	创建电影目录，将图片和文本放在该目录下
	'''
	mkdir(title)
        filname=title+'/'+title+'.png'
        savepic(filname,imag_url)
        with open(title+'/'+title+'.txt','a+',encoding='utf-8')as f:
            f.write('电影：{}\n {}\t {}\n {}\n 电影链接：{}\n'.format(title,actors,time,txx,links))
def main():
    url='http://dianying.2345.com/top/'
    get_content(url)

if __name__=='__main__':
    main()
