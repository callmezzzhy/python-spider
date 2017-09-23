# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
class BaikePipeline(object):
    def process_item(self, item, spider):
        base_dir=os.getcwd()
        filename=base_dir+'/'+'baike.txt'
        with open(filename,'a+') as f:
            f.write('作者：{} \n{}\n点赞：{}\t评论数：{}\n热评：{}\n'.format(item['author'], item['tag'], item['funs'], item['comnum'],item['hotpin']))
        #with open(item['author']+'1.png','wb')as f:
            #f.write(requests.get('https'+item['imgea']).content)
        return item
