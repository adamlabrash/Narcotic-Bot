import psycopg2
from scrapy.exceptions import NotConfigured


#Pipeline inputs each data item from scrape into a postgres db. Note that the postgres db and tables must already be initialized beforehand
class PostgresPipeline(object):
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host


    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")

        if not db_settings: # if we don't define db config in settings
            raise NotConfigured # then realise error

        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']

        return cls(db, user, passwd, host) # returning pipeline instance
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)


    #Connect to postgres db when spider is started
    def open_spider(self, spider):
        self.conn = psycopg2.connect(dbname=self.db,
                                    user=self.user, password=self.passwd,
                                    host=self.host)
        self.cursor = self.conn.cursor()


    #function will insert each data item into postgres db as it is scraped
    def process_item(self, item, spider):
        print(f"\nInserting {item.get('title')} into database...")

        try:
            sql = """INSERT INTO narcotics(title, website, sub_category, category, weight, weight_unit, price, purity, vendor, origin, ships_to, views, purchases, rating, quantity_remaining, date_of_offer, date_of_scrape, description, units_in_order, inventory_status, measurement_unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(sql,
                                (
                                    item.get("title"),
                                    item.get("website"),
                                    item.get("sub_category"),
                                    item.get("category"),
                                    item.get("weight"),
                                    item.get("weight_unit"),
                                    item.get("price"),
                                    item.get("purity"),
                                    item.get("vendor"),
                                    item.get("origin"),
                                    item.get("ships_to"),
                                    item.get("views"),
                                    item.get("purchases"),
                                    item.get("rating"),
                                    item.get("quantity_remaining"),
                                    item.get("date_of_offer"),
                                    item.get("date_of_scrape"),
                                    item.get("description"),
                                    item.get("units_in_order"),
                                    item.get("inventory_status"),
                                    item.get("measurement_unit")
                                )
                            )
            self.conn.commit()
            print("SUCCESS")
            return item
        except:
            print("Error inserting item into database")
            import pdb; pdb.set_trace()


    #Closes db connection when spider is done
    def close_spider(self, spider):
        self.conn.close()