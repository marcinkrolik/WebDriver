from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from pageobjects import *
import unittest, time, re, random

class Tc1(unittest.TestCase):
    '''
    This test cases creates new issue of bug type. It uses external csv file
    for test data storage. Test case is passed when submit did returned Dashboard object. 
    '''
    def readData(self, dataFile):
        data = {}
        for line in open(dataFile, 'r'):
            tmp = line.replace('\n','').split(';')
            data[tmp[0]] = tmp[1]
        return data 
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://jira.atlassian.com/"
        self.verificationErrors = []
        
    def test_tc1(self):
        driver = self.driver
        driver.get(self.base_url + "/login.jsp")
        #load test data
        data = self.readData('data.csv')
        #login
        login = LogIn(driver)
        dashboard = login.login(data['user'], data['passwd'])
        #open new issue popup
        issue = dashboard.createIssue(driver)
        #provide issue data
        issue.setType(data['itype'])
        issue.setSummary(data['summary'])
        issue.setPriority(data['prio'])
        issue.setDescription(data['desc'])
        #create issue
        dashboard = issue.submit()
        #check if returned object is of dashboard type (means issue creation went smooth)
        self.assertIsInstance(dashboard, Dashboard)
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
