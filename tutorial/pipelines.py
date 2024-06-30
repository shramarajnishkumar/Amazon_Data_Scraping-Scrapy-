# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class TutorialPipeline:
    def process_item(self, item, spider):
        return item

class MysqlAmazonPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'amazon_user',
            password = 'Password123#',
            database = 'amazon_db'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS amazon_data(
            id int NOT NULL auto_increment, 
            product_name text,
            product_price text,
            product_MRP text,
            product_img text,
            product_rating text,
            total_customer_rating text,
            product_page_url text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        print(f"==>> item: {item}")
        
        self.cur.execute("select * from amazon_data where product_name = %s", (item.get('product_name')[0],))
        result = self.cur.fetchone()
        
        if result:
            spider.logger.warn("Item already in database: %s" % item.get('product_name'))
        else:
            self.cur.execute(""" insert into amazon_data (product_name, product_price, product_MRP, product_img, product_rating, total_customer_rating, product_page_url) values (%s,%s,%s,%s,%s,%s,%s)""", (
                item["product_name"][0],
                item["product_price"][0],
                item["product_MRP"][0],
                item["product_img"][0],
                item["product_rating"][0],
                item["total_customer_rating"][0],
                item["product_page_url"][0]
            ))

            ## Execute insert of data into database
            self.conn.commit()
        return item
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
        
        
class MysqlAmazonProductPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'amazon_user',
            password = 'Password123#',
            database = 'amazon_db'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS amazon_product_details(
            id int NOT NULL auto_increment, 
            product_title text,
            product_rank text,
            product_description text,
            product_page_url text,
            product_image_url text,
            product_rating text,
            total_rated_users text,
            product_price text,
            deal_type text,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        try:
            self.cur.execute("SELECT * FROM amazon_product_details WHERE product_description = %s", (item.get('product_description')[0],))
            result = self.cur.fetchall()
            
            if len(result)>0:
                spider.logger.warn("Item already in database: %s" % item.get('product_title'))
            else:
                insert_query = """
                    INSERT INTO amazon_product_details (
                        product_title,
                        product_rank,
                        product_description,
                        product_page_url,
                        product_image_url,
                        product_rating,
                        total_rated_users,
                        product_price,
                        deal_type
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (
                    item["product_title"][0],
                    item["product_rank"][0],
                    item["product_description"][0],
                    item["product_page_url"][0],
                    item["product_image_url"][0],
                    item["product_rating"][0],
                    item["total_rated_users"][0],
                    item["product_price"][0],
                    item["deal_type"][0]
                )
                self.cur.execute(insert_query, data)
                self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        
        return item
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()