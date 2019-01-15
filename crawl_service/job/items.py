# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    TITLE = scrapy.Field()
    SALARY = scrapy.Field()
    LINK = scrapy.Field()
    COMPANY = scrapy.Field()
    ADDRESS = scrapy.Field()
    SKILL = scrapy.Field()
    TYPE = scrapy.Field()
    DEGREE = scrapy.Field()
    EXP = scrapy.Field()
