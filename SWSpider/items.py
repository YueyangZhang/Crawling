# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Flight(scrapy.Item):
    filename = scrapy.Field()
    x = scrapy.Field()
    y = scrapy.Field()
    depCity = scrapy.Field()
    arrCity = scrapy.Field()
    depDate = scrapy.Field()
    arrDate = scrapy.Field()
    flights = scrapy.Field()
    stops = scrapy.Field()
    price = scrapy.Field()
