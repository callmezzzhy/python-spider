# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs
import pymysql

class TianqiPipeline(object):
    def process_item(self, item, spider):
        base_dir=os.getcwd()
        filename=base_dir+'/xiamen.txt'
        with open(filename,'a+')as f:
            f.write('厦门天气：{}\n{}\n{}\n{}\n{}\n'.format(item['date'],item['week'],item['temperature'],item['weather'],item['wind']))
        for i in range(0,7):
            with open(base_dir+'/'+str(i)+'xm.png','wb')as f:
                f.write(requests.get(item['img']).content)



        return item
