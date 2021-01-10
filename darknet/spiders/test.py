# import scrapy
# import datetime
# from darknet.items import DarknetItem
# from darknet.sanitize import check_value, check_drug_type, isfloat
# import logging
# from scrapy.utils.response import open_in_browser
# # from darknet.captcha import solve_captcha
# from tbselenium.tbdriver import TorBrowserDriver
# from scrapy.http import HtmlResponse
# import pickle
# import time

# USERNAME = 'hellooo555'
# PASSWORD = 'zhsn79qgym'

# measurement_list = ['mg', 'mgs', 'ug', 'ugs', 'ml', 'l', 'g', 'gr', 'grams', 'pounds', 'lbs', 'ounce', 'oz']
# percent_list = ['%', 'percent', 'perc']

# # driver = TorBrowserDriver(tbb_path="/home/adam/Desktop/tor-browser_en-US/")


# URL = 'http://76p5k6gw25l5jpy7ombo2m7gt4zppowbz47sizvlzkigvnyhhc26znyd.onion'

# # URL = 'https://check.torproject.org'
# WEBSITE = "White House Market"

# class whiteHouseMarketSpider(scrapy.Spider):

#     handle_httpstatus_list = [301, 302]
#     name = 'whiteHouseMarket'
#     allowed_domains = ['76p5k6gw25l5jpy7ombo2m7gt4zppowbz47sizvlzkigvnyhhc26znyd.onion']
#     captcha_xpath = '/html/head/title/text()'
#     captcha_title = 'Robot Check'

#     def start_requests(self):

#         try:
#             print("Starting first request...")

#             yield scrapy.Request(url=URL, callback=self.parse)
#         except:
#             print("\nError proccessing URL\n")
#             logging.error(f'{WEBSITE}: URL error accessing main url        URL: {URL}        DATE: {str(datetime.datetime.now())}\n')
        

#     def parse(self, response):
#         # cookies = solve_captcha(response)

#         driver.get(response.url)
#         wait_for_user = input("Enter a character when captcha is solved and page is loaded: ")

#         #make it headless now
#         #login
#         if wait_for_user:
#             try:
#                 driver.find_element_by_xpath('/html/body/div[3]/div/form/div/input').click()
#             except:
#                 pass

#             time.sleep(1)
#             driver.find_element_by_xpath('/html/body/div[3]/form/div[1]/input').send_keys(USERNAME)
#             driver.find_element_by_xpath('/html/body/div[3]/form/div[2]/input').send_keys(PASSWORD)
#             driver.find_element_by_xpath('/html/body/div[3]/form/div[4]/input').click()
#             time.sleep(3)
#             driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div/button').click()
#             time.sleep(3)
#             for selection in range(1, 49):
#                 driver.get(response.url+f"/welcome?sc={selection}")

#                 for button in driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[5]/div/a")[1:-1]:
#                     driver.button.click()
#                     time.sleep(4)

#                     import pdb; pdb.set_trace()
#                     for product in driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[4]/div[2]/div"):
#                         print("Processing products...")
#                         text = product.text.split('\n')
#                         item = DarknetItem()
#                         item['website'] = "The White House Market"
#                         item['vendor'] = text[2]
#                         item['title'] = text[7]
#                         item['category'] = text[5]

#                         item['drug_type'] = check_drug_type(item['title'])
#                         item['weight'] = check_value(item['title'], measurement_list)
#                         item['purity'] = check_value(item['title'], percent_list)[0]
#                         item['views'] = None
#                         item['purchases'] = None
#                         item['price'] = text[9][4:] #gets rid of "USD"
#                         item['BTC_price'] = None
#                         item['origin'] = text[12][12:]
#                         item['ships_to'] = text[13][10:]
#                         item['rating'] = None
#                         item['quantity_remaining'] = text[8] #will be a string

#                         item['date_of_offer'] = product.xpath('./tr/td[2]/table[1]/tr/td/font//text()').extract()[-1][15:-2]
#                         item['date_of_scrape'] = str(datetime.datetime.now())

#                         print(f"\nSuccessfully extracted info for {item['title']}\n")
#                         return item

#         # for selection in range(1, 49): #cid is broad category (ie drugs, jewels, etc), scid is subcategory (ie Cannabis, Prescription, etc)
#         #     try:
#         #         print(f"Processing {response.url}?sc={selection}")
#         #         yield scrapy.Request(response.url+f"?sc={selection}", cookies=cookies, callback=self.parse_attr)
#         #     except:
#         #         print("\nError proccessing subcategory url\n")
#         #         logging.error(f'\n{WEBSITE}: URL broken for category URL: {response.url}/welcome?sc={selection}        DATE: {str(datetime.datetime.now())}\n')


#     '''Finished up to here'''
#     def parse_attr(self, response):

#         #follow each link at bottom of page
#         import pdb; pdb.set_trace()
#         if response.xpath('/html/body/table/tr/td[2]/div[2]/a/text()'):
#             for page in range(1, ((int(response.xpath('/html/body/table/tr/td[2]/div[2]/a/text()').extract()[-1]))+1)):
#                 try:
#                     print(f"Processing {response.url}+&page={page}")
#                     yield scrapy.Request(response.url+f"&page={page}", callback=self.parse_final)
#                 except:
#                     print("\nError proccessing pages within a subcategory\n")
#                     logging.error(f'\n{WEBSITE}: URL broken for subcategory pages        URL: {response.url}&page={page}      DATE: {str(datetime.datetime.now())}\n')
#         else:
#             print("\nUnable to find page number values\n")
#             logging.error(f"\n{WEBSITE}: Unable to find page number values        URL: {response.url}       DATE: {str(datetime.datetime.now())}\n")


#     def parse_final(self, response):

#         #figure out 100x2mg

#         measurement_list = ['mg', 'mgs', 'ug', 'ugs', 'ml', 'l', 'g', 'gr', 'grams', 'pounds', 'lbs', 'ounce', 'oz']
#         percent_list = ['%', 'percent', 'perc']

#         for product in response.xpath('/html/body/table/tr/td[2]/table'):
#             print("Processing products...")

#             item = DarknetItem()
#             item['website'] = "The Elite Market"
#             item['vendor'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/a/text()').extract()[0]
#             item['title'] = product.xpath('.//tr/td/b/a/text()').extract()[0]
#             item['category'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/text()').extract()[3][31:].strip()

#             item['drug_type'] = check_drug_type(item['title'])
#             item['weight'] = check_value(item['title'], measurement_list)
#             item['purity'] = check_value(item['title'], percent_list)[0]
            
#             temp_list = product.xpath('.//tr/td[2]/table[2]/tr/td[1]//text()').extract()
#             item['views'] = [temp_list[temp_list.index(x)+1] for x in temp_list if x == 'Views:'][0].strip()
#             item['purchases'] = [temp_list[temp_list.index(x)+1] for x in temp_list if x == 'Purchase:'][0].strip()

#             item['price'] = float(product.xpath('./tr/td[2]/table[2]/tr/td[3]/span/font[1]/text()').extract()[0][4:]) #gets rid of "USD"
#             item['BTC_price'] = float(product.xpath('.//tr/td[2]/table[2]/tr/td[3]/span/font[2]/text()').extract()[0][1:-1])
#             item['origin'] = product.xpath('.//tr/td[2]/table[2]/tr/td[2]/text()').extract()[1].strip()
#             item['ships_to'] = product.xpath('.//tr/td[2]/table[2]/tr/td[2]/text()').extract()[3].strip()
#             item['rating'] = product.xpath('./tr/td[2]/table[2]/tr/td[2]/a/font/text()').extract()[0].strip()[2:]

#             temp_list = product.xpath('.//tr/td[2]/table[2]/tr//text()').extract()
#             item['quantity_remaining'] = [temp_list[temp_list.index(x)+2] for x in temp_list if x == 'Quantity left:'][0].strip() #will be a string

#             item['date_of_offer'] = product.xpath('./tr/td[2]/table[1]/tr/td/font//text()').extract()[-1][15:-2]
#             item['date_of_scrape'] = str(datetime.datetime.now())

#             print(f"\nSuccessfully extracted info for {item['title']}\n")

#             if item['quantity_remaining'] == '':
#                 import pdb; pdb.set_trace()
#             return item

#     def solve_captcha(self, response):
#         print("HELLO")
#         if response.xpath(self.captcha_xpath).extract()[0] == self.captcha_title: #requires javascript
#             driver.get(response.url)
#             wait_for_user = input("Enter a character when captcha is solved and page is loaded: ")

#             if wait_for_user:
#                 # pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
#                 driver.switch_to_window(driver.window_handles[-1])
#                 body = driver.page_source
#                 return driver.get_cookies
#                 # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
#         else:
#             print("HELP")
#             return "No Cookies"
