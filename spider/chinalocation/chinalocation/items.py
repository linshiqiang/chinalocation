# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinalocationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Class1_Item(scrapy.Item):
    # 省级
    code = scrapy.Field()
    name = scrapy.Field()

class Class2_Item(scrapy.Item):
    # 市级
    code = scrapy.Field()
    name = scrapy.Field()

class Class3_Item(scrapy.Item):
    # 区级
    code = scrapy.Field()
    name = scrapy.Field()

class Class4_Item(scrapy.Item):
    # 街道
    code = scrapy.Field()
    name = scrapy.Field()

class Class5_Item(scrapy.Item):
    # 居委会
    code = scrapy.Field()
    code2 = scrapy.Field()
    name = scrapy.Field()