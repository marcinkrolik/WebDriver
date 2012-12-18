from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from pageobjects import *
import unittest, time, re, random

class Tc2(unittest.TestCase):
    '''
    This test case executes update of already existing issue.
    As a precondition TC1 must be executed first.
    This test case does not check if preconditions are fulfilled.    
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
        
    def test_tc2(self):
        driver = self.driver
        driver.get(self.base_url + "/login.jsp")
        data = self.readData('data.csv')
        #login
        login = LogIn(driver)
        dashboard = login.login(data['user'], data['passwd'])
        #switch to issues
        search = dashboard.searchIssue(driver)
        #serach for issues with given unique phrase
        results = search.newFilter(phrase = data['phrase'])
        #edit issue
        edited = results.editIssue(sum = data['summary'], newdesc = data['newdesc'])
        #check edited value
        val = edited.check(desc = data['newdesc'])
        self.assertTrue(val)
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
