import requests
from bs4 import BeautifulSoup

def get_url(url):
    try :
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return 'error'

def get_data(url,degree):
    for i in range(0,degree):
        urll=url+'&pn=' + str(50 * i)

        html=get_url(urll)
        soup=BeautifulSoup(html,'lxml')

        links=soup.find_all('li',attrs={'class':' j_thread_list clearfix'})

        for lin in links:

            try:
                title=lin.find('a',attrs={'class':'j_th_tit'}).text.strip()
                author=lin.find('span',attrs={'class':'tb_icon_author'})['title']
                link=url+lin.find('a',attrs={'class':'j_th_tit '})['href']
                time=lin.find('span',attrs={'class':'pull-right is_show_create_time'}).text.strip()
                tt=lin.find('span',attrs={'class':'threadlist_rep_num center_text'}).text.strip()
                info=('名字：{}\t回复数量：{}\n {}\t 发表时间：{}\t\n 贴吧链接：{}\t\n'.format(title,tt,author,time,link))
                with open('shuju.txt','a+',encoding='utf-8')as f:
                    f.write(info)
            except:
                return 'error'

def main():
    url='http://tieba.baidu.com/f?kw=生活大爆炸&ie=utf-8'
    y=int(input('请输入需要爬取多少页：'))
    get_data(url,y)
if __name__=='__main__':
    main()