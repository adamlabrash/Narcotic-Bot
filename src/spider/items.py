import scrapy

class DarknetItem(scrapy.Item):

    #mainly constant over lifetime of posting
    website = scrapy.Field()
    title = scrapy.Field()
    vendor = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    product_description = scrapy.Field()

    #consumer data
    views = scrapy.Field()
    purchases = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    comments = scrapy.Field()

    #location data
    shipping_origin = scrapy.Field()
    ships_to = scrapy.Field()

    #inventory data
    inventory_status = scrapy.Field()

    #measurement data
    measurement_unit = scrapy.Field()
    purity = scrapy.Field()
    total_weight = scrapy.Field()
    weight_per_unit = scrapy.Field()
    units_in_order = scrapy.Field() #how many pills

    date_of_posting = scrapy.Field()