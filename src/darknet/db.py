import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DB_NAME = os.environ.get('POSTGRES_DB')
USERNAME = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
PORT = os.environ.get('POSTGRES_PORT')

class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname=DB_NAME, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Error connecting to database. Exiting program...")
            exit(0)

    def insert(self, item):
        try:
            print(f"\nInserting {item.get('title')} into database...")

            sql = """INSERT INTO narcotics(title, website, sub_category, category, total_weight, weight_per_unit, price, purity, vendor, origin, ships_to, views, purchases, rating, quantity_remaining, date_of_offer, date_of_scrape, description, units_in_order, inventory_status, measurement_unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(sql,
                                (
                                    item.get("title"),
                                    item.get("website"),
                                    item.get("sub_category"),
                                    item.get("category"),
                                    item.get("total_weight"),
                                    item.get("weight_per_unit"),
                                    item.get("price"),
                                    item.get("purity"),
                                    item.get("vendor"),
                                    item.get("shipping_origin"),
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

    def create_db(self):
        self.cursor.execute(f'''CREATE database {DB_NAME}''')

    def close_connection(self):
        self.conn.close()