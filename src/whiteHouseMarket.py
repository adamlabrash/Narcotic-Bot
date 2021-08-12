import logging
from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os
from dotenv import load_dotenv, find_dotenv

from db import DB

load_dotenv(find_dotenv())

'''
TODO:
clean up code
run db
comment --> error handling specific exceptions
headless
logging

readme
'''

logging.basicConfig(filename="spider_log.txt", level=logging.ERROR)


class whiteHouseMarketSpider():

    def __init__(self, process_description=False):
        logging.info('----- STARTING WHITEHOUSE MARKET SPIDER -----')
        print('----- STARTING WHITEHOUSE MARKET SPIDER -----')

        self.username = os.environ.get("WHITE_HOUSE_USER")
        self.url = os.environ.get('WHITE_HOUSE_URL')
        self.password = os.environ.get("WHITE_HOUSE_PW")
        self.website = "White House Market"
        self.process_description = process_description

        self.db = DB()

        self.wait_time = 3  # how long the driver will wait for page to load

        tor_browser_path = os.environ.get("TOR_BROWSER_PATH")

        try:
            # self.driver = TorBrowserDriver(tbb_path=TOR_BROWSER_PATH)
            self.driver = TorBrowserDriver(
                tbb_path="/home/adam/Desktop/tor-browser_en-US/", tbb_logfile_path="./spider_log_verbose.txt")
        except Exception as e:
            print(
                'Error starting tor browser, make sure the path is correct in your .env file')
            exit(0)

        logging.info('\nSuccessfully initialized spider, starting parser\n')
        print('Initializing successful. Starting parser...')
        self.parse()

    def login(self):

        if not self.username or not self.password:
            print(
                f'Login credentials for {self.website} not found in .env file. You can enter them manually:')
            self.username = input(f'Please enter {self.website} username: ')
            self.password = input(f'Please enter {self.website} password: ')

        wait_for_user = input(
            "Enter a character when captcha is solved and page is loaded: ")

        # login
        if wait_for_user:

            # pop up
            try:
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div/form/div/input').click()
            except:
                pass

            # login
            print("Logging in")
            try:
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[1]/input').send_keys(self.username)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[2]/input').send_keys(self.password)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/form/div[4]/input').click()
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div/form/div/div[2]/div/button').click()
                self.driver.implicitly_wait(self.wait_time)
            except:
                print("ERROR LOGGING IN, TERMINATING PROGRAM")
                exit(0)

            print('Login successful')

    def parse(self):
        self.driver.get(self.url)
        self.login()
        self.driver.implicitly_wait(5)

        for selection in range(1, 50):
            print("Processing: " + self.url+f"/welcome?sc={selection}")
            self.driver.get(self.url+f"/welcome?sc={selection}")

            try:
                number_of_pages = int(self.driver.find_elements_by_xpath(
                    "/html/body/div/div/div/div[@class='panel panel-info']/div/strong")[0].text.split(' ')[-2])

            except Exception as e:
                import pdb
                pdb.set_trace()

            for page_number in range(number_of_pages+1):
                self.driver.get(
                    self.url+f"/welcome?sc={selection}&page={page_number}")
                try:
                    self.process_page()
                except Exception as e:
                    logging.error(
                        f'Error processing {self.url}/welcome?sc={selection}&page={page_number}: {e}')
        logging.info('Data extraction completed.')
        print('Data extraction completed. Ending program')
        exit(0)

    def process_page(self):
        print('Processing products...')

        if not self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div"):
            return

        for product in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div"):

            text = product.text.split('\n')
            item = {}
            item['website'] = self.website
            item['vendor'] = text[2]
            item['title'] = text[7]

            if len(text[5].split('-', 1)) != 1:
                item['category'] = text[5].split(
                    '-', 1)[0].strip()  # Opiods - Heroin --> Opiods
                item['sub_category'] = text[5].split(
                    '-', 1)[1].strip()  # --Heroin
            else:
                item['category'] = text[5]
                item['sub_category'] = 'Other'

            if text[9][:3] == "USD":
                item['price'] = float(text[9][3:])
            else:
                item['price'] = float(text[10][2:].split()[0])

            item['shipping_origin'] = text[12][12:]
            item['ships_to'] = text[13][10:]
            # in stock, low stock, out of stock
            item['inventory_status'] = text[8]

            if self.process_description:
                item = self.process_description(product, item)

            print(f"\nSuccessfully extracted info for {item['title']}\n")

            try:
                self.db.insert(item)
            except Exception as e:
                logging.error(f'Error inserting item into database: {e}')

    def process_description(self, product, item):
        print('Processing description page...')

        # go to description page
        try:
            product.find_element_by_xpath('./div/div[2]/a[2]').click()
            description = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div[4]/div[2]/textarea')))

            if len(description.text) < 998:
                item['product_description'] = description.text
            else:
                item['product_description'] = None

        except TimeoutException as e:
            print('Error processing description page. Moving on without description...')
            logging.error(
                f'Error processing description page for {item["title"]}: {e}')
            return item

        try:
            item['views'] = int(self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]').text[7:])  # what if item shows up in multiple categories?
            item['measurement_unit'] = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[4]').text[18:]

            description = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[4]/div[2]/textarea').text

        except:
            print("ERROR EXTRACTING DESCRIPTION")
            item['views'] = None
            item['description'] = None
            item['measurement_unit'] = None

        try:
            self.driver.back()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div/div/div/div')))
        except TimeoutException:
            pass

        return item


whiteHouseMarketSpider()
