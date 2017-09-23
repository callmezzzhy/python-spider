# -*- coding: utf-8 -*-
import scrapy
from tianqi.items import  TianqiItem
from scrapy.shell import inspect_response

class TtianqSpider(scrapy.Spider):
    name = 'ttianq'
    allowed_domains = ['tianqi.com']
    start_urls = ['http://xiamen.tianqi.com']

    def parse(self, response):

         '''
        筛选信息的函数：
        date = 今日日期
        week = 星期几
        img = 表示天气的图标
        temperature = 当天的温度
        weather = 当天的天气
        wind = 当天的风向
        '''

         items=[]
         sixday=response.xpath('//div[@class="tqshow1"]')
         for day in sixday:
             item=TianqiItem()
             date = ''
             for datetitle in day.xpath('./h3//text()').extract():
                 date += datetitle
             item['date'] = date
             item['week']=day.xpath('./p//text()').extract()[0]
             item['img']=day.xpath('./ul/li[@class="tqpng"]/img/@src').extract()[0]
             item['temperature']=''.join(day.xpath('./ul/li[2]//text()').extract()[0])
             item['weather']=day.xpath('./ul/li[3]//text()').extract()[0]
             item['wind'] = day.xpath('./ul/li[4]/text()').extract()[0]
             items.append(item)
             print(item['img'])
         return items
