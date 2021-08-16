#!/usr/bin/python
# -*- coding=utf-8 -*-
#encoding=utf-8
from os import sys
sys.path.append("..")
from imp import reload
reload(sys)
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
import time,os,pickle
import platform

class testWeb(object):

    def byIdSendKey(self,element,data):
        # global driver 
        driver.find_element_by_id(element).send_keys(data)

    def byNameSendKey(self,element,data):
        global driver 
        driver.find_element_by_Name(element).send_keys(data)    

    def byClassNameSendKey(self,element,data):
        global driver 
        driver.find_element_by_class_name(element).send_keys(data)    

    def byXpathSendKey(self,element,data):
        global driver 
        driver.find_element_by_xpath(element).send_keys(data) 

    def closeChrome(self):
        global driver
        driver.close()

    def visit(self,url):
        global driver
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')  
        if platform.system() == "Windows":
            slash = '\\'
            driver = webdriver.Chrome(executable_path = "C:\\Python37\chromedriver.exe",chrome_options = chrome_options)
        else:
            chrome_options.set_headless()
            driver = webdriver.Chrome(executable_path = "/usr/bin/chromedriver",chrome_options = chrome_options)
            slash = '/'     
        # driver = webdriver.Chrome(executable_path = "C:\\Python37\chromedriver.exe",chrome_options = chrome_options)
        driver.implicitly_wait(5)
        driver.maximize_window()
        driver.get(url)

    def getScreenshotAsFile(self,filename):
        global driver
        driver.get_screenshot_as_file(filename)

    def quitChrome(self):
        '''
            Quits the driver and closes every associated window. 
        '''
        global driver
        driver.quit()

    def findElementById(self,id):
        '''
            Location by ID
        '''
        global driver
        driver.find_element_by_id(id).click()

    def findElementByName(self,value):
        '''
            Location by name
        '''
        global driver
        driver.find_element_by_name(value).click()

    def findElementByClassName(self,value):
        '''
            Location by class name
        '''
        global driver
        driver.find_element_by_class_name(value).click()

    def findElementByTagName(self,value):
        '''
            Location by tag name
        '''
        global driver
        driver.find_element_by_tag_name(value).click()

    def findElementByXpath(self,value):
        '''
            Location by Xpath
        '''
        global driver
        driver.find_element_by_xpath(value).click() 

    def findElementByCssSelector(self,value):    
        '''
            Location by css
        '''
        global driver
        driver.find_element_by_css_selector(value).click()

    def findElementByLinkText(self,value):
        '''
            Location by link text
        '''
        global driver        
        driver.find_element_by_link_text(value).click()

    def findElementByPartialLinkText(self,value):
        '''
            Location by partial link text
        '''
        global driver        
        driver.find_element_by_partial_link_text(value).click()       

    def click():
        global driver        
        driver.click()

    def sendKey(value):
        global driver        
        driver.send_keys()

    def reflashChrome(self):
        '''
            Refresh browser current page
        '''  
        global driver
        driver.refresh()

    def executeScript(self,data):
        global driver
        driver.execute_script(data)

    def waitSleep(self,minute):
        '''
            time sleep
        '''  
        # print ("Start : %s" % time.ctime())
        time.sleep( minute )
        # print ("End : %s" % time.ctime())

    def backPage(self):
        '''
            Control browser Back
        '''
        global driver
        driver.back() 

    def forwardPage(self):
        '''
            Control browser forward
        '''
        global driver            
        driver.forward()
    def refreshBrowser(self):
        global driver
        driver.refresh()

    def clearIdTxt(self):
        '''
            clearTxt
        '''
        global driver            
        driver.find_element_by_id(id).clear()

    def clearNameTxt(self):
        '''
            clearTxt
        '''
        global driver            
        driver.find_element_by_name(id).clear()

    def switchFrame(self,data):
        global driver
        driver.switch_to.frame()

    def switchWindow(self,data):
        global driver
        driver.switch_to.window()

    def submitIdData(self):
        '''
            Submit Form
        '''
        global driver            
        driver.find_element_by_id(id).submit() 

    # def assertTitle(self):
    #     global driver
    #     res = driver.title
    #     return (res)  
        
    def assertUrl(self):
        global driver    
        res = driver.current_url
        return (res)

    def assertText(self,data):
        global driver
        res = driver.find_element_by_class_name(data).text
        return (res)    

    def watiElement(self, seconds):
        '''
            隐式等待
        '''
        self.driver.implicitly_wait(seconds)

# if __name__ == '__main__':
#     w = testWeb()
#     w.visit("https://www.baidu.com")
#     print(w.byIdSendKey("kw","selenium"))

