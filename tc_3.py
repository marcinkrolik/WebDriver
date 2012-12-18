from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from pageobjects import *
import unittest, time, re, random

class Tc3(unittest.TestCase):
    '''
    This test case executes Jira search for issues based on given phrase.
    '''
    def readData(self, dataFile):
        '''
        Simple function to slurp data from external csv file
        This is used to separate test data from test script
        '''
        data = {}
        for line in open(dataFile, 'r'):
            tmp = line.replace('\n','').split(';')
            data[tmp[0]] = tmp[1]
        return data 
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://jira.atlassian.com/"
        self.verificationErrors = []
        
    def test_tc3(self):
        driver = self.driver
        driver.get(self.base_url + "/login.jsp")
        data = self.readData('data.csv')
        #login
        login = LogIn(driver)
        dashboard = login.login(data['user'], data['passwd'])
        #serach for issues with given unique phrase
        search = dashboard.searchIssue(driver)
        #get rows with results
        rows = search.search(data['phrase'])
        #get reporter from rows
        results = search.getReporter(rows)
        #check if reporter matches
        for rep  in results:
            self.assertEqual(rep, data['user'])
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
