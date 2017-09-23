# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author=scrapy.Field()
    tag=scrapy.Field()
    funs=scrapy.Field()
    comnum=scrapy.Field()
    img=scrapy.Field()
    pageg=scrapy.Field()
    hotpin=scrapy.Field()

