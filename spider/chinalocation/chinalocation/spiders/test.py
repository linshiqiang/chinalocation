from pathlib import Path

from scrapy import *
from ..items import *
import re


class testSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        urls = [
            "https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/44.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/1101.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/01/110101.html
    # https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/11/01/01/110101001.html

    def parse(self, response):
        # 市级
        for node in response.xpath('//tr[@class="citytr"]'):
            item = Class2_Item()
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]
            url1 = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'
            url = url1 + node.xpath('./td[2]/a/@href').extract()[0]
            yield item
            yield Request(url, callback=self.parse3)

    def parse3(self, response):
        # 区级 towntr
        r=response.xpath('//tr[@class="countytr"]')+response.xpath('//tr[@class="towntr"]')
        for node in r:
            item = Class3_Item()
            name = node.xpath('./td[2]/a/text()').extract()
            if name :
                item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
                item['code'] = node.xpath('./td[1]/a/text()').extract()[0]
                url1 = response.request.url
                url1 = re.split('/\d+.html', url1)[0]
                url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
                yield item
                yield Request(url, callback=self.parse4)

    def parse4(self, response):
        # 街道
        for node in response.xpath('//tr[@class="towntr"]')+response.xpath('//tr[@class="villagetr"]'):
            item = Class4_Item()
            item['name'] = node.xpath('./td[2]/a/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/a/text()').extract()[0]

            url1 = response.request.url
            url1 = re.split('/\d+.html', url1)[0]

            url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
            yield item
            yield Request(url, callback=self.parse5)

    def parse5(self, response):
        # 居委会
        for node in response.xpath('//tr[@class="villagetr"]'):
            item = Class5_Item()
            item['name'] = node.xpath('./td[3]/text()').extract()[0]
            item['code'] = node.xpath('./td[1]/text()').extract()[0]
            item['code2'] = node.xpath('./td[2]/text()').extract()[0]
            yield item