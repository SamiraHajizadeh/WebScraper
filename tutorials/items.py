
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CoinItem(scrapy.Item):

  volume = scrapy.Field()
  no = scrapy.Field() ##
  reign = scrapy.Field()
  persons = scrapy.Field()
  city = scrapy.Field()
  region = scrapy.Field()
  province = scrapy.Field()
  denomination = scrapy.Field()
  average_weight = scrapy.Field()
  obverse = scrapy.Field() ##
  reverse = scrapy.Field() ##
  specimens = scrapy.Field() ##
  image_urls = scrapy.Field()
  images = scrapy.Field()