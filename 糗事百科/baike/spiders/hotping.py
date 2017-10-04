# -*- coding: utf-8 -*-
import scrapy
from baike.items import BaikeItem

class HotpingSpider(scrapy.Spider):
    name = 'hotping'
    allowed_domains = ['qiushibaike.com']
    start_urls = []
    for i in range(0,35):
        start_urls.append('https://www.qiushibaike.com/8hr/page/'+str(i)+'/')  #根据网站的特性，设置爬取页数

    def parse(self, response):
        item=BaikeItem()
        main=response.xpath('//div[@id="content-left"]/div')

        for lin in  main:
            item['img']=lin.xpath('./div[@class="author clearfix"]/a/img/@src')
            item['author']=lin.xpath('.//h2/text()').extract()[0]
            item['tag']=''.join( lin.xpath('a[@class="contentHerf"]/div/span[1]/text()').extract())
            item['funs']=lin.xpath('.//span[@class="stats-vote"]/i/text()').extract()[0]
            item['comnum']= lin.xpath('.//span[@class="stats-comments"]/a/i/text()').extract()[0]
            try:
                hot=''.join(lin.xpath('.//div[@class="cmtMain"]/div[1]/text()').extract())
            except:
                hot='暂无热评'
            item['hotpin']=hot
            try:
                im=lin.xpath('div[@class="thumb"]/a/img/@src')
            except:
                im='没有图片'
            item['pageg']=im
            yield item





