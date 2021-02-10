# from tbselenium.tbdriver import TorBrowserDriver
# from scrapy.http import HtmlResponse
# import pickle

# driver = TorBrowserDriver(tbb_path="/home/adam/Desktop/tor-browser_en-US/")


# def solve_captcha(response, spider):
#     if response.xpath(spider.captcha_xpath).extract()[0] == spider.captcha_title: #requires javascript
#         driver.get(response.url)
#         wait_for_user = input("Enter a character when captcha is solved and page is loaded: ")

#         if wait_for_user:
#             # pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
#             driver.switch_to_window(driver.window_handles[-1])
#             body = driver.page_source
#             return driver.get_cookies
#             # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
#     else:
#         print("HELP")
#         return "No Cookies"
#         # print(request.url)
#         # return response