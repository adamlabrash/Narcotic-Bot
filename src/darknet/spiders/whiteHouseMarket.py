import scrapy
from darknet.items import DarknetItem
from darknet.sanitize import check_value, check_drug_type, isfloat
from darknet.keywords import drug_list, measurement_list, unit_list, percent_list

import logging
from scrapy.utils.response import open_in_browser
from tbselenium.tbdriver import TorBrowserDriver
from scrapy.http import HtmlResponse

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

'''
TODO:
fix the lists
its skips the first page
it only does one product
clean up code
test sanitize
self.driver
'''

URL = os.environ.get('WHITE_HOUSE_URL')
USERNAME = os.environ.get("WHITE_HOUSE_USER")
PASSWORD = os.environ.get("WHITE_HOUSE_PW")
TOR_BROWSER_PATH = os.environ.get("TOR_BROWSER_PATH")
WEBSITE = "White House Market"

class whiteHouseMarketSpider(scrapy.Spider):

    handle_httpstatus_list = [301, 302]
    name = 'whiteHouseMarket'
    start_urls = [URL]

    def __init__(self):

        try:
            # self.driver = TorBrowserDriver(tbb_path=TOR_BROWSER_PATH)
            self.driver = TorBrowserDriver(tbb_path="/home/adam/Desktop/tor-browser_en-US/")

        except Exception as e:
            import pdb; pdb.set_trace()
            print('Error starting tor browser, make sure the path is correct in your .env file')


    def login(self):

        import pdb; pdb.set_trace()
        if not USERNAME or not PASSWORD:
            print(f'Login credentials for {WEBSITE} not found in .env file. You can enter them manually:')
            USERNAME = input(f'Please enter {WEBSITE} username: ')
            PASSWORD = input(f'Please enter {WEBSITE} password: ')

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
                self.driver.implicitly_wait(8)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[1]/input').send_keys(USERNAME)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[2]/input').send_keys(PASSWORD)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/div[4]/input').click()
                self.driver.implicitly_wait(8)
                self.driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div/button').click()
                self.driver.implicitly_wait(8)
            except:
                print("ERROR LOGGING IN, TERMINATING PROGRAM")
                exit(0)

    def parse(self, response):
        self.driver.get(response.url) #yield process(self.driver.get(response.url))
        self.login()

        # for selection in range(1, 49):
        for selection in range(1, 2):
            button = self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[5]/div/a[@class='btn btn-primary spacebutton']")[:-1].text #get last button value

            #for page in range(button)

            print("Processing: " + response.url+f"/welcome?sc={selection}")
            
            self.driver.get(response.url+f"/welcome?sc={selection}")
            self.driver.implicitly_wait(8)
            import pdb; pdb.set_trace()

            for button in buttons:
                yield process_page()
                # print("Clicking button " + button.text)
                # button.click()
                # time.sleep(8)

                # for product in driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[4]/div[2]/div"):
                #     text = product.text.split('\n')
                #     item = DarknetItem()
                #     item['website'] = WEBSITE
                #     item['vendor'] = text[2]
                #     item['title'] = text[7]

                #     if text[5].split('-', 1)[1]:
                #         item['category'] = text[5].split('-', 1)[0].strip() #Opiods - Heroin --> Opiods
                #         item['sub_category'] = text[5].split('-', 1)[1].strip() #--Heroin
                #     else:
                #         item['category'] = text[5]
                #         item['sub_category'] = 'Other'
                    
                #     #only collect weight values of herion, cocaine, crystal, etc --> not pills
                #     if item['sub_category'] != 'Other' or item['category'] != None:
                #         weight_info = check_value(item['title'], measurement_list)
                #         item['weight'] = weight_info[0]
                #         item['weight_unit'] = weight_info[1]
                #         item['purity'] = check_value(item['title'], percent_list)[0]

                #         #default = 1 --> how many pills are ordered
                #         unit_info = check_value(item['title'], [['x']])
                #         if(unit_info == (None, None)):
                #             item['units_in_order'] = 1
                #         else:
                #             item['units_in_order'] = int(unit_info[0])
                #     else:
                #         item['weight'] = None
                #         item['weight_unit'] = None
                #         item['purity'] = None

                #     if text[9][:3] == "USD":
                #         item['price'] = float(text[9][3:])
                #     else:
                #         item['price'] = float(text[10][2:].split()[0])
                        
                #     item['origin'] = text[12][12:]
                #     item['ships_to'] = text[13][10:]
                #     item['date_of_scrape'] = str(datetime.datetime.now())
                #     item['quantity_remaining'] = None
                #     item['inventory_status'] = text[8] #in stock, low stock, out of stock

                #     #go to description page
                #     product.find_element_by_xpath('./div/div[2]/div[2]/a[2]').click()
                #     time.sleep(6)
                #     #next page
                #     item['purchases'] = None
                #     item['date_of_offer'] = None
                #     item['rating'] = None #available with vendor info --> maybe scrape vendors

                #     try:
                #         item['views'] = int(driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]').text[7:]) #what if item shows up in multiple categories?
                #         item['description'] = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[4]/div[2]/textarea').text
                #         item['measurement_unit'] = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[4]').text[18:]
                #     except:
                #         print("ERROR EXTRACTING DESCRIPTION")
                #         item['views'] = None
                #         item['description'] = None
                #         item['measurement_unit'] = None

                #     driver.back()
                #     time.sleep(6)

                #     print(f"\nSuccessfully extracted info for {item['title']}\n")
                #     yield item

    def process_page(self):
        for product in self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[4]/div[2]/div"):
            text = product.text.split('\n')
            item = DarknetItem()
            item['website'] = WEBSITE
            item['vendor'] = text[2]
            item['title'] = text[7]

            if text[5].split('-', 1)[1]:
                item['category'] = text[5].split('-', 1)[0].strip() #Opiods - Heroin --> Opiods
                item['sub_category'] = text[5].split('-', 1)[1].strip() #--Heroin
            else:
                item['category'] = text[5]
                item['sub_category'] = 'Other'
            
            #only collect weight values of herion, cocaine, crystal, etc --> not pills
            if item['sub_category'] != 'Other' or item['category'] != None:
                weight_info = check_value(item['title'], measurement_list)
                item['weight'] = weight_info[0]
                item['weight_unit'] = weight_info[1]
                item['purity'] = check_value(item['title'], percent_list)[0]

                #default = 1 --> how many pills are ordered
                unit_info = check_value(item['title'], [['x']])
                if(unit_info == (None, None)):
                    item['units_in_order'] = 1
                else:
                    item['units_in_order'] = int(unit_info[0])
            else:
                item['weight'] = None
                item['weight_per_unit'] = None
                item['purity'] = None

            if text[9][:3] == "USD":
                item['price'] = float(text[9][3:])
            else:
                item['price'] = float(text[10][2:].split()[0])
                
            item['origin'] = text[12][12:]
            item['ships_to'] = text[13][10:]
            item['quantity_remaining'] = None
            item['inventory_status'] = text[8] #in stock, low stock, out of stock

            #go to description page
            product.find_element_by_xpath('./div/div[2]/div[2]/a[2]').click()
            self.driver.implicitly_wait(8)
            #next page
            item['purchases'] = None
            item['date_of_offer'] = None
            item['rating'] = None #available with vendor info --> maybe scrape vendors

            try:
                item['views'] = int(self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]').text[7:]) #what if item shows up in multiple categories?
                item['description'] = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[4]/div[2]/textarea').text
                item['measurement_unit'] = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[4]').text[18:]
            except:
                print("ERROR EXTRACTING DESCRIPTION")
                item['views'] = None
                item['description'] = None
                item['measurement_unit'] = None

            self.driver.back()
            self.driver.implicitly_wait(8)

            print(f"\nSuccessfully extracted info for {item['title']}\n")
            yield item