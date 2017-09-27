from zhua12360 import station
from 邮箱 import post
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
ssl._create_default_https_context=ssl._create_unverified_context()
requests.packages.urllib3.disable_warnings()
code_dict={v:k for k,v in station.items()}

def get_cok(url):

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    r=requests.get(url,headers=headers,verify=False)
    cookie_list = r.cookies
    return cookie_list
def get_api_url(text):
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
    info_list=[]
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    cookie={'Cookie':'JSESSIONID={}; route={}; BIGipServerotn={}; fp_ver=4.5.1; RAIL_EXPIRATION=1506554681887; RAIL_DEVICEID=Kq5_42IONBjhC6a6fjsrWwRTsIr3AjP4CjtX4RVJzh_lYdQBX0VjryKUgqp2BYhSOAaJiyGEkTuUisxAUavArGaoGJli9zH92a-B58ZPaBqdNtwwD3tbexaKBaAhuCtFK1tCiutK5DcuOibV726Ve6Ktc6_peH_4; _jc_save_fromStation=%u4ED9%u6E38%2CXWS; _jc_save_toStation=%u53A6%u95E8%2CXMS; _jc_save_fromDate=2017-10-01; _jc_save_toDate=2017-10-07; _jc_save_wfdc_flag=wf'.format(js,rt,bigsr)}
    r=requests.get(url,headers=headers,cookies=cookie,verify=False)
    print(r)
    try:
        db=pymysql.connect("localhost","root","123456","12306api",use_unicode=True,charset="utf8")
        cursor=db.cursor()
        sql2="DELETE FROM 12306cepiao"
        sql="alter table 12306cepiao auto_increment =1"
        cursor.execute(sql2)
        cursor.execute(sql)
        db.commit()
    finally:
        db.close()
    try:
        #r=requests.get(url,headers=headers,verify=False)
        #print(r)
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
            print(start_time)
            arrive_time=data_list[9]
            print(arrive_time)
            time_fucked_up=data_list[10]
            print(time_fucked_up)
            first_seat=data_list[31]or'--'
            print(first_seat)
            second_seat=data_list[30]or'--'
            print(second_seat)
            soft_seat=data_list[23]or'--'
            print(soft_seat)
            hard_seat=data_list[28]or'--'
            print(hard_seat)
            no_seat=data_list[26]or'--'
            print(no_seat)

            info=('车次:{}\n出发站:{}\t目的地:{}\n出发时间:{}\t到达时间:{}\t消耗时间:{}\t座位情况：\n 一等座：「{}」 \t二等座：「{}」\t软卧：「{}」\t硬座：「{}」\t无座：「{}」\n'.format(train_num, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_seat,second_seat, soft_seat,hard_seat, no_seat))
            #print(info)
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
        return info_list
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
    content=get_cok(url)
    l=dict(content)
    js=l['JSESSIONID']
    rt=l['route']
    bgsr=l['BIGipServerotn']
    text=input("请输入要查询车票信息：")
    info=train_info(get_api_url(text),js,rt,bgsr)
    for content in info:
        with open('车票查询.txt','a+')as f:
            f.write(content)
    #post()
if __name__=='__main__':
    main()




