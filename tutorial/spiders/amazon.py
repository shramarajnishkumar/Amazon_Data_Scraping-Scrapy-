import scrapy
from pathlib import Path
import json
from scrapy.selector import Selector
from tutorial.items import AmazonData


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    q = "ipad 9th generation tempered glass"
    start_urls = [f"https://www.amazon.in/s?k={q}"]

    def parse(self, response):
        data = response.css('div.sg-col-inner span div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16')
        for each in data:
            product_page_url = each.css('div.sg-col-inner div.celwidget span div.puis-card-container div.a-section div.puisg-row div.puisg-col div.puisg-col-inner div.s-product-image-container div.aok-relative span a::attr(href)').extract_first()
            product_image_url = each.css('div.sg-col-inner div.celwidget span div.puis-card-container div.a-section div.puisg-row div.puisg-col div.puisg-col-inner div.s-product-image-container div.aok-relative span a div.a-section img::attr(src)').extract_first()
            right_section = each.css('div.sg-col-inner div.celwidget span div.puis-card-container div.a-section div.puisg-row div.puisg-col.puis-list-col-right div.puisg-col-inner div.a-section.a-spacing-small.a-spacing-top-small')
            product_name = right_section.css('div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style h2 span::text').extract_first()
            product_rating = right_section.css('div.a-section.a-spacing-none.a-spacing-top-micro div.a-row.a-size-small span::attr(aria-label)').extract_first()
            rating_customer = right_section.css('div.a-section.a-spacing-none.a-spacing-top-micro div.a-row.a-size-small span::attr(aria-label)').extract()
            total_rating_customer = '0'
            if len(rating_customer)>0:
                total_rating_customer = rating_customer[1]
                
            product_price_section = right_section.css('div.puisg-row div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 div.puisg-col-inner')
            start_product_price = product_price_section.css('div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style div.a-row.a-size-base.a-color-base a span.a-price span.a-offscreen::text').extract_first()
            close_product_price = product_price_section.css('div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style div.a-row.a-size-base.a-color-base a span.a-price span::text').extract_first()
            product_price = None
            if start_product_price == close_product_price:
                 product_price = start_product_price
            else:
                product_price = start_product_price+' - '+ close_product_price    
            product_MRP = product_price_section.css('div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style div.a-row.a-size-base.a-color-base a div span.a-price.a-text-price span.a-offscreen::text').extract_first()
            # product_offer = product_price_section.css('div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style div.a-row.a-size-base.a-color-base').extract()
            # print(f"==>> product_offer: {product_offer}")
            complete_url_product_page = response.urljoin(product_page_url) 
            
            
            # print("===============", complete_url_product_page)
            # yield response.follow(complete_url_product_page, callback=self.parse_next_page)
            amazon_db = AmazonData()
            amazon_db["product_name"]= product_name,
            amazon_db["product_price"]= product_price,
            amazon_db["product_MRP"]= product_MRP,
            amazon_db["product_img"]= product_image_url,
            amazon_db["product_rating"]= product_rating,
            amazon_db["total_customer_rating"]= total_rating_customer,
            amazon_db["product_page_url"]= complete_url_product_page,
            yield amazon_db
            # yield {
            #     "product_name": product_name,
            #     "product_price": product_price,
            #     "product_MRP": product_MRP,
            #     "product_img": product_image_url,
            #     "product_rating": product_rating,
            #     "total_customer_rating": total_rating_customer,
            #     "product_page_url" : complete_url_product_page,
            # }
    
    def parse_next_page(self, response):
        print(f"==>> new_page: {response}")
        data = response.css('div#a-page div#dp div#dp-container div#ppd div#leftCol div#imageBlock').extract()
        print(f"==>> data: {data}")
        pass
