# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


from scrapy.item import Item, Field

class AmazonData(Item):
    product_name = Field()
    product_price = Field()
    product_MRP = Field()
    product_img = Field()
    product_rating = Field()
    total_customer_rating = Field()
    product_page_url = Field()
    
class AmazonProductData(Item):
    product_title = Field()
    product_rank = Field()
    product_description = Field()
    product_page_url = Field()
    product_image_url = Field()
    product_rating = Field()
    total_rated_users = Field()
    product_price = Field()
    deal_type = Field()
