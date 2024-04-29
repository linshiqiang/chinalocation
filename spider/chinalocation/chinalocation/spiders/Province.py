from pathlib import Path

from scrapy import *
from ..items import *
import re


class ProvinceSpider(scrapy.Spider):
    name = "Province"

    def start_requests(self):
        urls = [
            "https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/1101.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/01/110101.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/01/01/110101001.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/44/4420.html

    def parse(self, response):
        # 省级
        for node in response.xpath('//tr[@class="provincetr"]/td'):
            item = Class1_Item()
            item['code'] = node.xpath('./a/@href').extract()[0].split('.')[0]
            item['name'] = node.xpath('./a/text()').extract()[0]
            url1 = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'#/sj/tjbz/tjyqhdmhcxhfdm/2023/
            url = url1 + node.xpath('./a/@href').extract()[0]
            yield item
            yield Request(url, callback=self.parse2, dont_filter=True)
            
    def parse2(self, response):
        # 市级
        for node in response.xpath('//tr[@class="citytr"]'):
            item = Class2_Item()
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]
            url1 = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'
            url = url1 + node.xpath('./td[2]/a/@href').extract()[0]
            yield item
            yield Request(url, callback=self.parse3, dont_filter=True)
            
    # 只统计到了区级
    def parse3(self, response):
        # 区级 towntr 
        # 存在直辖镇故此处调整towntr; https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/44/4420.html
        r=response.xpath('//tr[@class="countytr"]')+response.xpath('//tr[@class="towntr"]')
        for node in r:
            item = Class3_Item()
            name = node.xpath('./td[2]/a/text()').extract()
            if name :
                item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
                item['code'] = node.xpath('./td[1]/a/text()').extract()[0]

                url1 = response.request.url
                url1 = re.split(r'/\d+.html', url1)[0]

                url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
                yield item
                # yield Request(url, callback=self.parse4, dont_filter=True)
                # 只统计到了区级;
        
    def parse4(self, response):
        # 街道
        for node in response.xpath('//tr[@class="towntr"]'):
            item = Class4_Item()
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]

            url1 = response.request.url
            url1 = re.split(r'/\d+.html', url1)[0]

            url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
            yield item
            yield Request(url, callback=self.parse5, dont_filter=True)

    def parse5(self, response):
        # 居委会
        for node in response.xpath('//tr[@class="villagetr"]'):
            item = Class5_Item()
            item['name'] = node.xpath('./td[3]/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/text()').extract()[0]
            item['code2'] = node.xpath('./td[2]/text()').extract()[0]
            yield item
