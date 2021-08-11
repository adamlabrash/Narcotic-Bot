from items import DarknetItem
from sanitize import check_value, check_drug_type, isfloat
from keywords import drug_list, measurement_list, unit_list, percent_list

import logging
from tbselenium.tbdriver import TorBrowserDriver

import os
from dotenv import load_dotenv, find_dotenv

from db import DB

load_dotenv(find_dotenv())

'''
TODO:
fix the lists
clean up code
test sanitize
'''



class whiteHouseMarketSpider():

    def __init__(self):

        self.username = os.environ.get("WHITE_HOUSE_USER")
        self.url = os.environ.get('WHITE_HOUSE_URL')
        self.password = os.environ.get("WHITE_HOUSE_PW")
        self.website = "White House Market"

        self.db = DB()

        self.wait_time = 2 #how long the driver will wait for page to load

        tor_browser_path = os.environ.get("TOR_BROWSER_PATH")

        try:
            # self.driver = TorBrowserDriver(tbb_path=TOR_BROWSER_PATH)
            self.driver = TorBrowserDriver(tbb_path="/home/adam/Desktop/tor-browser_en-US/", tbb_logfile_path="./spider_log.txt")
        except Exception as e:
            print('Error starting tor browser, make sure the path is correct in your .env file')
            exit(0)

        print('Starting parser...')
        self.parse()


    def login(self):

        if not self.username or not self.password:
            print(f'Login credentials for {self.website} not found in .env file. You can enter them manually:')
            self.username = input(f'Please enter {self.website} username: ')
            self.password = input(f'Please enter {self.website} password: ')

        wait_for_user = input("Enter a character when captcha is solved and page is loaded: ")

        #login
        if wait_for_user:

            #pop up
            try:
                self.driver.find_element_by_xpath('/html/body/div[3]/div/form/div/input').click()
            except:
                pass

            #login
            print("Logging in")
            try:
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[1]/input').send_keys(self.username)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[2]/input').send_keys(self.password)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[4]/input').click()
                self.driver.implicitly_wait(self.wait_time)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div/button').click()
                self.driver.implicitly_wait(self.wait_time)
            except:
                print("ERROR LOGGING IN, TERMINATING PROGRAM")
                exit(0)

    def parse(self):
        self.driver.get(self.url)
        self.login()

        # for selection in range(1, 49):
        for selection in range(1, 2):
            print("Processing: " + self.url+f"/welcome?sc={selection}")
            self.driver.get(self.url+f"/welcome?sc={selection}")
            
            try:
                number_of_pages = int(self.driver.find_elements_by_xpath("/html/body/div/div/div/div[@class='panel panel-info']/div/strong")[0].text.split(' ')[-2])
            except Exception:
                import pdb; pdb.set_trace()

            for page_number in range(number_of_pages):
                self.driver.get(self.url+f"/welcome?sc={selection}&page={page_number}")
                self.process_page()

    def process_page(self):
        print('Processing products...')

        for product in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div"):
            text = product.text.split('\n')
            item = {}
            item['website'] = self.website
            item['vendor'] = text[2]
            item['title'] = text[7]

            if text[5].split('-', 1)[1]:
                item['category'] = text[5].split('-', 1)[0].strip() #Opiods - Heroin --> Opiods
                item['sub_category'] = text[5].split('-', 1)[1].strip() #--Heroin
            else:
                item['category'] = text[5]
                item['sub_category'] = 'Other'
            

            if text[9][:3] == "USD":
                item['price'] = float(text[9][3:])
            else:
                item['price'] = float(text[10][2:].split()[0])
                
            item['origin'] = text[12][12:]
            item['ships_to'] = text[13][10:]
            item['inventory_status'] = text[8] #in stock, low stock, out of stock

            try:
                item = self.process_description(self, product, item)
            except Exception as e:
                pass

            print(f"\nSuccessfully extracted info for {item['title']}\n")
            import pdb; pdb.set_trace()
            self.db.insert(item)

    def process_description(self, product, item):
        print('Processing description page...')

        #go to description page
        product.find_element_by_xpath('./div/div[2]/div[2]/a[2]').click()
        self.driver.implicitly_wait(self.wait_time)

        try:
            item['views'] = int(self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]').text[7:]) #what if item shows up in multiple categories?
            item['description'] = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[4]/div[2]/textarea').text
            item['measurement_unit'] = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[4]').text[18:]
        except:
            print("ERROR EXTRACTING DESCRIPTION")
            item['views'] = None
            item['description'] = None
            item['measurement_unit'] = None
            import pdb; pdb.set_trace()
        
        self.driver.back()

        return item


whiteHouseMarketSpider()