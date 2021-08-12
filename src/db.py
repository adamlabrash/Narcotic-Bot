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
            self.conn = psycopg2.connect(
                dbname=DB_NAME, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()

        except Exception as e:
            print("Error connecting to database. Exiting program...")
            exit(0)

    def insert(self, item):
        try:
            print(f"\nInserting {item.get('title')} into database...")
            self.cursor.execute(f"insert into narcotics (%s) values (%s)" % (
                ','.join(item), ','.join('%%(%s)s' % k for k in item)), item)

            return item

        except:
            print("Error inserting item into database")
            import pdb
            pdb.set_trace()
