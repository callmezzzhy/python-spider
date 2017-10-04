from zhua12360 import station
from qqsmtp import post
import test311
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
from selenium import webdriver
from tkinter import *
import tkinter.messagebox as messagebox
import time
import os
import sys
import pymysql



import ssl
'''
12306采用的是https协议,而ssl证书是它自己做的并没有得到浏览器的认可,所以Python默认是不会请求不受信任的证书的网站的
所有通过这行代码来关闭掉证书的验证
'''
ssl._create_default_https_context=ssl._create_unverified_context()   
requests.packages.urllib3.disable_warnings()  
code_dict={v:k for k,v in station.items()}           #全部车站名信息

def get_cok(url):
    '''
    因为12306的网站在利用其开放的api进行查询余票时会cookies进行验证，而且每隔一会，cookies就会失效，
    所以我在这里先用requests请求进入余票查询网页来自动获取该网页的cookies
    用来对后面需要请求余票系统api的时候进行cookies验证
    '''
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    r=requests.get(url,headers=headers,verify=False)
    cookie_list = r.cookies
    return cookie_list
def get_api_url(text):
    
    '''
    构造所查询的余票信息url
    '''
    args=str(text).split(' ')
    print(args)
    try:
        date=args[0]
        from_station_name=args[1]
        to_station_name=args[2]
        from_station=station[from_station_name]
        to_station=station[to_station_name]
    except:
        date,from_station,to_station='--','--','--'


    url = (
        'https://kyfw.12306.cn/otn/leftTicket/queryX?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
    print(url)
    return url
def train_info(url,js,rt,bigsr):
    
    
    '''
    余票查询
    '''
    info_list=[]
    '''
    构造headers，cookies，以便可以正常进入12306余票系统查询
    这里的cookie就是上面我们自动获取到的
    而且因为我们每次进入余票查询系统的时候都会先去网页自动获取cookie
    所以保证了cookie不会因为时间太久失效了
    '''
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    cookie={'Cookie':'JSESSIONID={}; route={}; BIGipServerotn={}; fp_ver=4.5.1; RAIL_EXPIRATION=1506554681887; RAIL_DEVICEID=Kq5_42IONBjhC6a6fjsrWwRTsIr3AjP4CjtX4RVJzh_lYdQBX0VjryKUgqp2BYhSOAaJiyGEkTuUisxAUavArGaoGJli9zH92a-B58ZPaBqdNtwwD3tbexaKBaAhuCtFK1tCiutK5DcuOibV726Ve6Ktc6_peH_4; _jc_save_fromStation=%u4ED9%u6E38%2CXWS; _jc_save_toStation=%u53A6%u95E8%2CXMS; _jc_save_fromDate=2017-10-01; _jc_save_toDate=2017-10-07; _jc_save_wfdc_flag=wf'.format(js,rt,bigsr)}
    r=requests.get(url,headers=headers,cookies=cookie,verify=False) #忽略SSL验证
    print(r)
    '''
    这里我利用pymsql来对本地的mysql进行连接，并将获取到的余票信息都保存在数据库里
    以便后续我们的使用
    '''
    try:
        db=pymysql.connect("localhost","root","123456","12306api",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        '''
        每一次连接数据库后要写数据前，我都把先前的表内容都删除掉，以免数据库的信息缓存了太多没用的信息
        保证了每一次写进数据库里都是最新的余票信息
        方便我们查找
        '''
        sql2="DELETE FROM 12306cepiao"
        '''
        因为建表时，id是自动增加的，虽然每次都删除数据了，但是每次重新写数据时，id还是在不断增加，这样肯定是不行的
        所以在这里我又设置了每次删除数据后，id也自动从1开始增加
        '''
        sql="alter table 12306cepiao auto_increment =1"
        cursor.execute(sql2)
        cursor.execute(sql)
        db.commit()
    finally:
        db.close()
        '''
        这里就是我们正式获取余票信息的查找，因为是json文件，所以在之前进行了一次json文件的读取
        '''
    try:
        #r=requests.get(url,headers=headers,verify=False)
        #print(r)
        second={}
        start={}
        raw_trains=r.json()['data']['result']
        print(raw_trains)
        print('正在：')
        for raw_train in raw_trains:
            data_list=raw_train.split('|')
            print(data_list)
            train_num=data_list[3]
            print(train_num)
            from_station_code=data_list[6]
            from_station_name=code_dict[from_station_code]
            print(from_station_name)
            to_station_code=data_list[7]
            to_station_name=code_dict[to_station_code]
            print(to_station_name)
            start_time=data_list[8]
            start[train_num]=start_time
            print(start_time)
            arrive_time=data_list[9]
            print(arrive_time)
            time_fucked_up=data_list[10]
            print(time_fucked_up)
            first_seat=data_list[31]or'--'
            print(first_seat)
            second_seat=data_list[30]or'--'
            second[train_num]=second_seat
            print(second_seat)
            soft_seat=data_list[23]or'--'
            print(soft_seat)
            hard_seat=data_list[28]or'--'
            print(hard_seat)
            no_seat=data_list[26]or'--'
            print(no_seat)

            info=('车次:{}\n出发站:{}\t目的地:{}\n出发时间:{}\t到达时间:{}\t消耗时间:{}\t座位情况：\n 一等座：「{}」 \t二等座：「{}」\t软卧：「{}」\t硬座：「{}」\t无座：「{}」\n'.format(train_num, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_seat,second_seat, soft_seat,hard_seat, no_seat))
            #print(info)
            '''
            连接本地数据库，把获取到的数据都保存在数据库中
            '''
            
            try:
                db=pymysql.connect("localhost","root","123456","12306api",use_unicode=True,charset="utf8")
                cursor=db.cursor()
                sql1="""INSERT INTO 12306cepiao(train_num, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_seat,second_seat, soft_seat,hard_seat, no_seat)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(sql1,(train_num, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_seat,second_seat, soft_seat,hard_seat, no_seat))
                db.commit()
            finally:
                db.close()
            info_list.append(info)
        return info_list,second,start
    except:
        return '噢噢，出现错误啦！'
'''
root = Tk()

#定义键盘时间，敲击键盘，会被打印

def key(event):
    print ("pressed", repr(event.char))
    i=repr(event.char)
    i=i.replace('\'','')
    with open ('hostb.txt','a+') as fb:
        fb.write(i)
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    content=get_cok(url)
    l=dict(content)
    js=l['JSESSIONID']
    rt=l['route']
    bgsr=l['BIGipServerotn']
    with open('hostb.txt','r')as f:
        text=f.read()
    info=train_info(get_api_url(text),js,rt,bgsr)
    for content in info:
        with open('车票查询.txt','a+')as f:
            f.write(content)
#定义save按钮的点击事件，保存内容到文件当中

def saveClick(event):
   pass


frame = Frame(root, width=300, height=300)
frame.pack()

#在frame中定义text空间
text=Text(frame)

#放入默认的文案
text.insert(INSERT,"this is text……")

#为text bind事件
text.bind("<Key>",key)
text.pack()

#定义button按钮
button=Button(frame,text='save')

#为按钮绑定事件
button.bind("<Button>",saveClick)
button.pack()
root.mainloop()'''


def main():
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    '''
    这里主要是调用get_cok函数来获取cookie
    因为获取到cookie是多串字符组成的
    我把它字典化，然后根据key—value
    找到每次cookie刷新时的几个key的value，并保存在 js，rt，bgsr里
    再将这3个参数传到train_info函数里
    '''
    content=get_cok(url)
    l=dict(content)
    js=l['JSESSIONID']
    rt=l['route']
    bgsr=l['BIGipServerotn']
    text=input("请输入要查询车票信息：")
    starttime=int(input("请输入查询车票最早始发整点时间："))
    endtime=int(input("请输入查询车票最晚始发整点时间："))
    '''
    这里我简单将查询到的二等座对应车次的信息保存在了second，车次对应的发车时间保存在了time
    根据用户输入想查询的发车时间段，提取出有用的车次信息，然后根据车次信息去second字典里提出二等座的座位情况
    判断二等座是否为：无或者‘--’信息，如果不是则输出车次，发车时间和二等座剩余信息，保存在inff列表里
    假如inff有append信息，调用发邮箱函数，将这些信息及时通过邮箱发送给用户
    '''
    info,second,time=train_info(get_api_url(text),js,rt,bgsr)
    inff=[]
    for key ,value in time.items():
        va=(str(value).split(':'))[0]
        if int(va) in range(starttime,endtime):
                if not sencond[key] =='无'or not sencond[key]=='--':
                    inf1=("车次:{} 发车时间：{} 二等座剩余：{}".format(key,value,sencond[key]))
                    inff.append(inf1)
    if not inff==[]:                
        post(inff)
    print(inff)
    for content in info:
        with open('车票查询.txt','a+')as f:
            f.write(content)
    
if __name__=='__main__':
    main()




