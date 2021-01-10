# import scrapy
# import datetime
# from darknet.items import DarknetItem
# from darknet.sanitize import check_value, check_drug_type, isfloat, measurement_list, percent_list
# import logging

# URL = 'http://elite6c3wh756biv7v2fyhnoitizvl2gmoisq7xgmp2b2c5ryicottyd.onion'
# '''
# elite6c3wh756biv7v2fyhnoitizvl2gmoisq7xgmp2b2c5ryicottyd.onion
# elitejnmwyc6sfrsb4tqlxxl36m2uegrj3kxvjtsms2lbolytihlxxid.onion
# elitemk4vggs2zlx7rjdc7hrkvrm6bslyetxwfyo5kt2yykgz5yg4wyd.onion
# eliteuzdzrsc3nqe3hmbwh3ccoij6q5qvaonk2et7c35egqhytdtm4ad.onion
# elitewrywbnvoud3sbhkuiot6a4oouyvqxlufakbscojlq2keqz3yvid.onion
# elitexwoy625pr3yofvd5vcshceypmpbywtwlvudqmv5oepombom4wyd.onion
# '''

# WEBSITE = "Elite Market"

# class eliteMarketSpider(scrapy.Spider):

#     handle_httpstatus_list = [301, 302]
#     name = 'eliteMarket'
#     allowed_domains = ['elite6c3wh756biv7v2fyhnoitizvl2gmoisq7xgmp2b2c5ryicottyd.onion']

#     def start_requests(self):

#         try:
#             print("Starting first request...")
#             yield scrapy.Request(url=URL, callback=self.parse)
#         except:
#             print("\nError proccessing URL\n")
#             logging.error(f'{WEBSITE}: URL error accessing main url        URL: {URL}        DATE: {str(datetime.datetime.now())}\n')
        

#     def parse(self, response):
#         print("HELLO")
#         for selection in range(6, 15): #cid is broad category (ie drugs, jewels, etc), scid is subcategory (ie Cannabis, Prescription, etc)
#             try:
#                 print(f"Processing {response.url}/index.php?cid=2&scid={selection}")
#                 yield scrapy.Request(response.url+f"/index.php?cid=2&scid={selection}", callback=self.parse_attr)
#             except:
#                 print("\nError proccessing subcategory url\n")
#                 logging.error(f'\n{WEBSITE}: URL broken for category URL: {response.url}/index.php?cid=2&scid={selection}        DATE: {str(datetime.datetime.now())}\n')

#     def parse_attr(self, response):
#         #follow each link at bottom of page
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

#         for product in response.xpath('/html/body/table/tr/td[2]/table'):
#             print("Processing products...")

#             item = DarknetItem()
#             item['website'] = "The Elite Market"
#             item['vendor'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/a/text()').extract()[0]
#             item['title'] = product.xpath('.//tr/td/b/a/text()').extract()[0]
#             item['category'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/text()').extract()[3][31:].strip()

#             item['drug_type'] = check_drug_type(item['title'])

#             weight_info = check_value(item['title'], measurement_list)
#             item['weight'] = weight_info[0]
#             item['weight_unit'] = weight_info[1]

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

#         # try:
#         #     for product in response.xpath('/html/body/table/tr/td[2]/table'):
#         #         item = DarknetItem()
#         #         item['website'] = "The Elite Market"
#         #         item['vendor'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/a/text()').extract()[0]
#         #         item['title'] = product.xpath('.//tr/td/b/a/text()').extract()[0]
#         #         item['category'] = product.xpath('.//tr/td[2]/table[1]/tr/td/font/text()').extract()[3][31:].strip()

#         #         item['drug_type'] = check_drug_type(item['title'])
#         #         item['weight'] = check_value(item['title'], measurement_list)
#         #         item['purity'] = check_value(item['title'], percent_list)[0]
                
#         #         temp_list = product.xpath('.//tr/td[2]/table[2]/tr/td[1]//text()').extract()
#         #         item['views'] = [temp_list[temp_list.index(x)+1] for x in temp_list if x == 'Views:'][0].strip()
#         #         item['purchases'] = [temp_list[temp_list.index(x)+1] for x in temp_list if x == 'Purchase:'][0].strip()

#         #         item['price'] = float(product.xpath('./tr/td[2]/table[2]/tr/td[3]/span/font[1]/text()').extract()[0][4:]) #gets rid of "USD"
#         #         item['BTC_price'] = float(product.xpath('.//tr/td[2]/table[2]/tr/td[3]/span/font[2]/text()').extract()[0][1:-1])
#         #         item['origin'] = product.xpath('.//tr/td[2]/table[2]/tr/td[2]/text()').extract()[1].strip()
#         #         item['ships_to'] = product.xpath('.//tr/td[2]/table[2]/tr/td[2]/text()').extract()[3].strip()
#         #         item['rating'] = product.xpath('./tr/td[2]/table[2]/tr/td[2]/a/font/text()').extract()[0].strip()[2:]

#         #         temp_list = product.xpath('.//tr/td[2]/table[2]/tr//text()').extract()
#         #         item['quantity_remaining'] = [temp_list[temp_list.index(x)+1] for x in temp_list if x == 'Quantity left:'][0].strip() #will be a string

#         #         item['date_of_offer'] = product.xpath('./tr/td[2]/table[1]/tr/td/font//text()').extract()[-1][15:-2]
#         #         item['date_of_scrape'] = str(datetime.datetime.now())

#         #         print(f"\nSuccessfully extracted info for {item['title']}\n")
#         #         return item
#         # except:
#         #     print("\nXPATH error\n")
#         #     import pdb; pdb.set_trace()
#         #     logging.error(f"\n{WEBSITE}: XPATH error with extracting info        URL: {response.url}        DATE: {str(datetime.datetime.now())}\n")
#         #     return