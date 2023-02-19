# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ACitem(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
