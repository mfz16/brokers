# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import time
from scrapy.selector import Selector
from selenium import webdriver
import selenium as sel
from scrapy.http import FormRequest
from loginform import fill_login_form
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from movie.items import AcresItem

# shell command to run:
# $ scrapy crawl movie_budget -o movie_budget.json
ur='https://www.99acres.com/rent-property-in-pune-ffid?orig_property_type=R&class=O&search_type=QS&pageid=QS&clsrc=owner_tab'
class MovieBudgetSpider(scrapy.Spider):
    name = "acres"
    allowed_domains = ["www.99acres.com"]
    #uri='https://www.99acres.com/rent-property-in-pune-ffid?orig_property_type=R&class=O&search_type=QS&pageid=QS&clsrc=owner_tab'
    uri='https://www.99acres.com/rent-property-in-PUNE-ffid'
    #start_urls = (
    #    'https://www.99acres.com/search/dealer/rent/residential/pune?search_type=QS&search_location=CP19&lstAcn=CP_R&lstAcnId=19&src=CLUSTER&preference=R&selected_tab=6&city=19&res_com=R&isvoicesearch=N&keyword_suggest=pune%3B&fullSelectedSuggestions=pune&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsicHVuZSIsIkNJVFlfMTksIFBSRUZFUkVOQ0VfUiwgUkVTQ09NX1IiXX1d&texttypedtillsuggestion=pune&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_19%2C%20PREFERENCE_R%2C%20RESCOM_R&searchform=1&price_min=null&price_max=null',
    #)
    start_urls = ["https://www.99acres.com/property/loginpage.php"]
    login_user = "farazshine786@gmail.com"
    login_pass = "f1r1z.16"


    def __init__(self):

        #self.driver = webdriver.Firefox(executable_path=r'E:\firefoxgecko\geckodriver.exe')
        #self.driver.get('http://inventwithpython.com')

        self.driver=webdriver.Chrome()
        #self.driver.fullscreen_window()

    def parse(self, response):
        print"responce is",response.url
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        foo = response.headers['Set-Cookie']
        print "foo is" ,foo
        values = {k.strip(): v for k, v in re.findall(r'(.*?)=(.*?);', foo)}
        print "values",values
        #self.driver.add_cookie(values)

        tmpCookie = response.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
        print 'cookie from login', tmpCookie
        cookieHolder = dict(SESSION_ID=tmpCookie)
        return FormRequest(url, method=method, formdata=args, callback=self.after_login)
    def after_login(self, response):
        ids=[]
        #self.driver.get(ur)
        cross=[]

        self.driver.get("https://www.99acres.com/property/loginpage.php")
        time.sleep(2)
        username = self.driver.find_element_by_name("username")
        print "yuyuyuyu",username
        username.send_keys("farazshine786@gmail.com")
        password = self.driver.find_element_by_name("password")

        password.send_keys("f1r1z.16")
        login_attempt = self.driver.find_element_by_xpath("//input[@value='Login >>']")
        login_attempt.click()

        time.sleep(3)
        window_before = self.driver.window_handles[0]
        self.driver.get(ur)
        time.sleep(2)
        next = self.driver.find_element_by_css_selector('.filter-arrowDown')
        #next.click()
        self.driver.execute_script("arguments[0].click();", next)
        next=self.driver.find_element_by_xpath("//label[@for='spm2']")
        #next.click()
        self.driver.execute_script("arguments[0].click();", next)
        time.sleep(3)
        prop_blocks=self.driver.find_elements_by_xpath("//div[@title='View property details']")
        print "propblo",prop_blocks[0]
        print "propblo", prop_blocks[1]
        prop_id=[]
        j=0
        for i in prop_blocks:
            prop_id.append(i.get_attribute("data-propid"))
            j=j+1
        print "j is",j
        print "prop is",prop_id
        if('viewJ31387947'=='view'+prop_id[0]):
            print "matched"
        time.sleep(3)


        base_link = 'https://www.99acres.com'
        rows_in_big_table = response.css('.vpn::text').extract()
        print "rows1", rows_in_big_table
        #next = self.driver.find_element_by_css_selector('.vpn')
        #print "next is",next.click()
        #time.sleep(2.5)
        while True:
            try:

                next = self.driver.find_elements_by_css_selector('.vpn')
                print "next is",next
                url = ur
                #window_before = self.driver.window_handles[0]
                #print "window before",window_before
                count=0
                for i in next:
                    print "elemen is  ",i.get_attribute("id")
                    ids.append(i.get_attribute("id"))


                #yield Request(url, callback=self.parse2)
                print "total phone",next
                page_count=1
                while(page_count<680):
                    for i in range(0,len(ids)):
                        print"before  click"
                        print "now i is  ",i
                        #webdriver.ActionChains(webdriver.Chrome()).move_to_element(next[i]).click(next[i]).perform()
                        #self.driver.execute_script("arguments[0].scrollIntoView;", next[i])

                        #next[i].click()
                        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_id(ids[i]))

                        #self.driver.execute_script("arguments[0].click();", next)

                        print"after click"
                        time.sleep(5)
                        #window_after = self.driver.window_handles[1]

                        #print "window after manual click", window_before
                        #next1 = self.driver.find_elements_by_css_selector('.eoi_contactInfo1')
                        if(count==0):
                            contact=self.driver.find_element_by_css_selector('.eoiLyr_form')
                            rad=self.driver.find_element_by_css_selector('.eoiLyr_individualOpt')
                            rad.click()
                            time.sleep(1)
                            sub=self.driver.find_element_by_css_selector('.eoiLyr_formBtn')
                            time.sleep(2)
                            sub.click()
                            time.sleep(2)
                            count=1
                        time.sleep(5)
                        ph=self.driver.find_element_by_xpath('//div[@id="genlayer'+ids[i]+'"]//div[@class="eoi_contactInfo"]')
                        print "phone no  ",ph.text
                        ph = self.driver.find_element_by_xpath('//div[@id="genlayer'+ids[i]+'"]//div[@class="eoi_contacts"]')
                        print "name and email  ", ph.text
                        time.sleep(2)
                        #if self.driver.find_element_by_css_selector('.layerCross').is_displayed():
                        cr=self.driver.find_element_by_xpath('//div[@id="genlayer'+ids[i]+'"]/div/i')
                        #cr=self.driver.find_element_by_css_selector('.layerCross')
                        #crs=self.driver.find_element_by_css_selector('.eoi_vsplayer').get_attribute('id')
                        print "crs attribute",cr
                        print i+1, "before clicked cross and its id  is"
                        print "cr is",cr

                        #element = WebDriverWait(cr[-1], 10).until(

                            #EC.presence_of_element_located((By.CSS_SELECTOR, ".layerCross"))

                       # )
                        #cr.click()
                        window_after = self.driver.switch_to.window(window_before)
                        self.driver.execute_script("arguments[0].click();", cr)
                        #next[i].send_keys(webdriver.common.keys.Keys.SPACE)
                        print i+1,"after times clicked cross",
                        time.sleep(5)
                        #self.driver.implicitly_wait(10)a
                        #next = self.driver.find_elements_by_css_selector('.vpn')
                        #self.driver.switch_to.default_content()
                    #self.driver.switch_to.default_content()
                    #contact = self.driver.find_element_by_name("oauth2relay895134551")
                    #self.driver.switch_to.frame(0)
                    #print "name of frame",contact.get_attribute("id")
                    #print "no of iframes", contact
                    #s = sel.get_text(".eoi_contactInfo")
                    #print "s is                           ", s
                    #next1.click()
                    #print "radio is              ",self.driver.find_element_by_css_selector('.eoiLyr_individualOpt'),"    kjl    "
                    # Do some crawling of javascript created content with Selenium
                    page_count+=1
                    next=self.driver.find_element_by_xpath("//a[@value="+str(page_count)+"]")
                    self.driver.execute_script("arguments[0].click();", next)
                    #next.click()
                    time.sleep(3)
            except Exception, err:
                print "errrrrrrrrrrrrr      "
                print Exception,err
                break

        self.driver.close()
        print "=" * 50
        rows_in_big_table = response.css('.b::text').extract()
        print "rows",rows_in_big_table
        # now we only consider rows with odd index number, namely, skip useless rows
        items = []
        for i in rows_in_big_table:
            items=AcresItem()

            print "hello-"

            vary=response.xpath('//input[@id="filter_name"].text()')
            items['varx']=i

            print "=" * 50

