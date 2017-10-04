import requests
from bs4 import BeautifulSoup
import os

def get_html(url):

    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return 'error'

def get_url(url):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    links=soup.find_all('div',class_='index_toplist mright mbottom') #除了历史分类外其他类型所有小说信息
    urls=[]
    nname=[]
    comment={}
    history=soup.find_all('div',class_='index_toplist  mbottom') #历史分类下的小说信息
    
    '''
    各个类型的小说名和链接保存在表格里
    '''
    for lin in links:

        name=lin.find('div',class_='toptab').span.string
        with open('novel_list.csv', 'a+') as f:
            f.write("\n小说种类：{} \n".format(name))
        total_list=lin.find(style='display: block;')
        book_list=total_list.find_all('li')
        for book in book_list:

            title = book.a['title']
            comment[title] = 'http://www.qu.la' + book.a['href']
            urls.append(comment)
            nname.append(title)

            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{} \t 小说地址：{} \n".format(title, comment[title]))

    for his in history:
        names=his.find('div',class_='toptab').span.string
        with open('novel_list.csv','a')as f:
            f.write("\n小说：{}\n".format(names))
        his_book=his.find(style='display: block;')
        for hst in his_book:
            titles=hst.a['title']
            comment[titles]='http://www.qu.la' + hst.a['href']
            urls.append(comment)
            nname.append(titles)
            with open('novel_list.csv','a')as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(titles,comment[titles]))

    return urls,nname,comment
def get_text(url,textname):

    url_list=[]
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    ll=soup.find_all('dd')
    print(ll)
    #textname=soup.find('div',id='info').h1.text
    #textname=soup.find('h1').text
    #print(textname)
    '''
    找到当篇小说所有章节的链接地址
    '''
    with open('小说{}.txt'.format(textname),'a')as f:
        f.write(textname)
    for url in ll:
        url_list.append('http://www.qu.la'+ url.a['href'])

    return textname,url_list
def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = get_html(url).replace('<br/>', '\n')
    print(html)
    soup = BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        title = soup.find('title').text

        with open('{}.txt'.format(title), 'a+',encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(txt)
        print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')
def main():
    url='http://www.qu.la/paihangbang/'
    '''
    在列出的所有小说里找到自己想要下载的小说“择天记”
    并下载保存在本地
    '''
    ll,na,dic=get_url(url)
    for i in na:
        if i=='择天记':
            lin=dic[i]
            print(lin)
            nm,uurl=get_text(lin,i)
            print(uurl)
            if not os.path.exists(nm):
                os.mkdir(nm)
            for url in uurl:
                get_one_txt(url,nm)
if __name__=='__main__':
    main()
