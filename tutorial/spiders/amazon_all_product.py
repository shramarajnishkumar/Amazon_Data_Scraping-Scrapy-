import scrapy
import json
import os
from tutorial.items import AmazonProductData


class AmazonAllProductSpider(scrapy.Spider):
    name = "amazon_all_product"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/"]

    def parse(self, response):
        navbar_link = response.css('div#a-page header div#navbar div#nav-main div.nav-fill div#nav-xshop-container div#nav-xshop a::attr(href)')
        amazon_miniTV = response.urljoin(navbar_link[0].extract())
        sell = response.urljoin(navbar_link[1].extract())
        best_sellers = response.urljoin(navbar_link[2].extract())
        today_deals = response.urljoin(navbar_link[3].extract())
        mobiles = response.urljoin(navbar_link[4].extract())
        customer_service = response.urljoin(navbar_link[5].extract())
        electronics  = response.urljoin(navbar_link[6].extract())
        new_releases  = response.urljoin(navbar_link[7].extract())
        home_kitchen  = response.urljoin(navbar_link[9].extract())
        gift_ideas  = response.urljoin(navbar_link[10].extract())
        fashion  = response.urljoin(navbar_link[11].extract())
        amazon_pay  = response.urljoin(navbar_link[12].extract())
        computers  = response.urljoin(navbar_link[13].extract())
        books  = response.urljoin(navbar_link[14].extract())
        beauty_personal_care  = response.urljoin(navbar_link[15].extract())
        Coupons  = response.urljoin(navbar_link[16].extract())
        toys_games  = response.urljoin(navbar_link[17].extract())
        home_improvement  = response.urljoin(navbar_link[18].extract())
        sports_fitness_outdoors  = response.urljoin(navbar_link[19].extract())
        gift_cards  = response.urljoin(navbar_link[20].extract())
        grocery_gourmet_foods  = response.urljoin(navbar_link[21].extract())
        health_household_personal_care  = response.urljoin(navbar_link[22].extract())
        car_motorbike  = response.urljoin(navbar_link[23].extract())
        baby  = response.urljoin(navbar_link[24].extract())
        subscribe_save  = response.urljoin(navbar_link[25].extract())
        video_games  = response.urljoin(navbar_link[26].extract())
        pet_supplies  = response.urljoin(navbar_link[27].extract())
        audible  = response.urljoin(navbar_link[28].extract())
        AmazonBasics  = response.urljoin(navbar_link[29].extract())
        kindle_eBooks  = response.urljoin(navbar_link[30].extract())
        links = [
            best_sellers,
            new_releases
        ]
        for link in links:
            if link == best_sellers:
                yield response.follow(best_sellers, callback=self.parse_best_sellers_page)
            elif link == new_releases:
                yield response.follow(new_releases, callback=self.parse_new_releases_page)
            else:
                pass

    
    def parse_best_sellers_page(self, response):
        data = response.css('div#a-page div#zg div#zg_colmask div#zg_colleft div#zg_col1wrap div#zg_col1')
        header_title = data.css('div.celwidget.c-f div._p13n-zg-banner-landing-page-header_style_zgLandingPageBanner__15GAl div._p13n-zg-banner-landing-page-header_style_zgLandingPageBannerTitleContainer__3pQqv span#zg_banner_text::text').extract_first()
        header_sub_title = data.css('div.celwidget.c-f div._p13n-zg-banner-landing-page-header_style_zgLandingPageBanner__15GAl div._p13n-zg-banner-landing-page-header_style_zgLandingPageBannerTitleContainer__3pQqv span#zg_banner_subtext::text').extract_first()
        best_seller_product = data.css('div#zg_left_colmask div#zg_left_colleft div#zg_left_col2 div.celwidget.c-f div._p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz div._p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf._p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL')
        
        best_seller_product_url = best_seller_product.css('a::attr(href)').extract()
        best_seller_product_url_title = best_seller_product.css('a::text').extract()
        for url in best_seller_product_url:
            yield response.follow(url, callback=self.parse_best_sellers_product_page)
            
    def parse_best_sellers_product_page(self, response):
        try:
            data = response.css('div#a-page div#zg div.a-fixed-left-flipped-grid div.a-fixed-left-grid-inner div#zg-right-col div.celwidget.c-f div')
            title = data.css('div._cDEzb_card-title_2sYgw h1::text').extract_first()
            products = data.css('div.a-cardui._cDEzb_card_1L-Yx div.p13n-desktop-grid div.p13n-gridRow._cDEzb_grid-row_3Cywl div#gridItemRoot')
            product_data = []
            for product in products:
                product_details = product.css('div.a-cardui._cDEzb_grid-cell_1uMOS.expandableGrid.p13n-grid-content div._cDEzb_iveVideoWrapper_JJ34T')
                product_rank = product_details.css('div.a-section.zg-bdg-ctr div.a-section.zg-bdg-body.zg-bdg-clr-body.aok-float-left span.zg-bdg-text::text').extract_first()
                product_description = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal')[1].css('span div::text').extract_first()
                product_page_url = response.urljoin(product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal::attr(href)').extract_first())
                product_image_url = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal div.a-section.a-spacing-mini._cDEzb_noop_3Xbw5 img::attr(src)').extract_first()
                product_rating = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row div.a-icon-row a.a-link-normal i span.a-icon-alt::text').extract_first()
                total_rated_users = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row div.a-icon-row a.a-link-normal span.a-size-small::text').extract_first()
                if product_rating:
                    product_price = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row')[-1].css('a.a-link-normal span.a-color-secondary span.a-size-base span.p13n-sc-price::text').extract_first()
                product_price = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row a.a-link-normal span.a-color-secondary span.a-size-base span.p13n-sc-price::text').extract_first()
                
                amazon_product = AmazonProductData()
                amazon_product["product_title"] = title,
                amazon_product["product_rank"] = product_rank,
                amazon_product["product_description"] = product_description,
                amazon_product["product_page_url"] = product_page_url,
                amazon_product["product_image_url"] = product_image_url,
                amazon_product["product_rating"] = product_rating,
                amazon_product["total_rated_users"] = total_rated_users,
                amazon_product["product_price"] = product_price,
                amazon_product["deal_type"] = "Best Sellers",
                yield amazon_product
            #     product_data.append({
            #         "product_title": title,
            #         "product_rank": product_rank,
            #         "product_description": product_description,
            #         "product_page_url": product_page_url,
            #         "product_image_url": product_image_url,
            #         "product_rating": product_rating,
            #         "total_rated_users": total_rated_users,
            #         "product_price": product_price,
            #     })
                
            # filename = f'{title.replace(' ', '_')}.json'  
            # file_path = f"tutorial/amazon_best_sellers/{filename}"   
            # directory = os.path.dirname(file_path)
            # if not os.path.exists(directory):
            #     os.makedirs(directory)
            # with open(file_path, 'a', encoding='utf-8') as file:
            #     json.dump(product_data, file, ensure_ascii=False, indent=4)  
            next_page_url = response.urljoin(data.css('div.a-cardui._cDEzb_card_1L-Yx div.a-text-center ul.a-pagination li.a-last a::attr(href)').extract_first())
            yield response.follow(next_page_url, callback=self.parse_best_sellers_product_page) 
        except Exception as e:
            print(e)
            
    def parse_new_releases_page(self, response):
        deal_title = response.css('div#a-page div#zg div#zg_colmask div#zg_colleft div#zg_col1wrap div#zg_col1 div.celwidget.c-f div._p13n-zg-banner-landing-page-header_style_zgLandingPageBanner__15GAl span#zg_banner_text::text').extract_first()
        deal_sub_title = response.css('div#a-page div#zg div#zg_colmask div#zg_colleft div#zg_col1wrap div#zg_col1 div.celwidget.c-f div._p13n-zg-banner-landing-page-header_style_zgLandingPageBanner__15GAl span#zg_banner_subtext::text').extract_first()
        new_release_inks = response.css('div#a-page div#zg div#zg_colmask div#zg_colleft div#zg_col1wrap div#zg_col1 div#zg_left_colmask div#zg_left_colleft div#zg_left_col2 div.celwidget.c-f div._p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz div._p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf._p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL a::attr(href)').extract()
        for new_release in new_release_inks:
            yield response.follow(response.urljoin(new_release), callback=self.parse_new_releases_product_page)
            
    def parse_new_releases_product_page(self, response):
        try:
            data = response.css('div#a-page div#zg div.a-fixed-left-flipped-grid div.a-fixed-left-grid-inner div#zg-right-col div.celwidget.c-f')
            product_page_title = data.css('h1::text').extract_first()
            products = data.css('div.p13n-desktop-grid div.p13n-gridRow._cDEzb_grid-row_3Cywl div#gridItemRoot')
            product_data = []
            for product in products:
                product_details = product.css('div.a-cardui._cDEzb_grid-cell_1uMOS.expandableGrid.p13n-grid-content div._cDEzb_iveVideoWrapper_JJ34T')
                rank = product_details.css('div.a-section.zg-bdg-ctr div.a-section.zg-bdg-body.zg-bdg-clr-body.aok-float-left span.zg-bdg-text::text').extract_first()
                description = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal')[1].css('span div::text').extract_first()
                product_page_link = response.urljoin(product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal::attr(href)').extract_first())
                product_img_link = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout a.a-link-normal')[0].css('div.a-section.a-spacing-mini._cDEzb_noop_3Xbw5 img::attr(src)').extract_first()
                product_rating = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row a.a-link-normal i span::text').extract_first()
                total_rated_users = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row a.a-link-normal span.a-size-small::text').extract_first()
                if product_rating:
                    product_price = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row')[-1].css('a.a-link-normal span.a-color-secondary span.a-size-base span.p13n-sc-price::text').extract_first()
                product_price = product_details.css('div.zg-grid-general-faceout div.p13n-sc-uncoverable-faceout div.a-row a.a-link-normal span.a-color-secondary span.a-size-base span.p13n-sc-price::text').extract_first()
                amazon_product = AmazonProductData()
                amazon_product["product_title"] = product_page_title,
                amazon_product["product_rank"] = rank,
                amazon_product["product_description"] = description,
                amazon_product["product_page_url"] = product_page_link,
                amazon_product["product_image_url"] = product_img_link,
                amazon_product["product_rating"] = product_rating,
                amazon_product["total_rated_users"] = total_rated_users,
                amazon_product["product_price"] = product_price,
                amazon_product["deal_type"] = "New Releases",
                yield amazon_product
            #     product_data.append({
            #             "product_title": product_page_title,
            #             "product_rank": rank,
            #             "product_description": description,
            #             "product_page_url": product_page_link,
            #             "product_image_url": product_img_link,
            #             "product_rating": product_rating,
            #             "total_rated_users": total_rated_users,
            #             "product_price": product_price,
            #         })
                
            # filename = f'{product_page_title.replace(' ', '_')}.json'  
            # file_path = f"tutorial/amazon_new_release/{filename}"   
            # directory = os.path.dirname(file_path)
            # if not os.path.exists(directory):
            #     os.makedirs(directory)
            # with open(file_path, 'a', encoding='utf-8') as file:
            #     json.dump(product_data, file, ensure_ascii=False, indent=4) 
            
            next_page_url = response.urljoin(data.css('div.a-cardui._cDEzb_card_1L-Yx div.a-text-center ul.a-pagination li.a-last a::attr(href)').extract_first())
            yield response.follow(next_page_url, callback=self.parse_new_releases_product_page)  
        except Exception as e:
            print(e)
        
        
        









