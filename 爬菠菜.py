import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return 'error'

def get_data(url):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    bisai=soup.find_all('div',class_='matchmain bisai_qukuai')
    print(bisai)
    for link in bisai:
        time=link.find('div',class_='whenm').text.strip()
        name=link.find_all('span',class_='team_name')

        if name[0].string[0:3]=='php':
            team1_name='无队名'
        else:
            team1_name=name[0].text.strip()
        level=link.find('span',class_='team_number_green').text.strip()
        team2_name=name[1].text.strip()
        llevel=link.find('span',class_='team_number_red').text.strip()
        info=('比赛时间：{}，\n 队伍一：{}      胜率 {}\n 队伍二：{}      胜率 {} \n'.format(time,team1_name,level,team2_name,llevel))
        print(info)
        with open('bocai.txt','a+',encoding='utf-8')as f:
            f.write(info)

def main():
    url= 'http://dota2bocai.com/match'
    get_data(url)
if __name__=='__main__':
    main()