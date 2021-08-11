from .db import DB

#Pipeline inputs each data item from scrape into a postgres db
class PostgresPipeline(object):
    def __init__(self):
        self.db = DB()

    def process_item(self, item, spider):
        self.db.insert(item)

    def close_spider(self, spider):
        self.db.conn.close()