# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DarknetItem(scrapy.Item):
    website = scrapy.Field()
    vendor = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    views = scrapy.Field()
    purchases = scrapy.Field()
    price = scrapy.Field()
    origin = scrapy.Field()
    ships_to = scrapy.Field()
    weight = scrapy.Field()
    weight_unit = scrapy.Field()
    rating = scrapy.Field()
    quantity_remaining = scrapy.Field()
    date_of_offer = scrapy.Field()
    date_of_scrape = scrapy.Field()
    units_in_order = scrapy.Field() #how many pills
    inventory_status = scrapy.Field()
    purity = scrapy.Field()
    description = scrapy.Field()
    measurement_unit = scrapy.Field()