from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

class LogIn(object):
    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("login-form-username").is_enabled())
    
    def login(self, user, passwd):
        self.driver.find_element_by_id("login-form-username").clear()
        self.driver.find_element_by_id("login-form-username").send_keys("marcinkrolik")
        self.driver.find_element_by_id("login-form-password").clear()
        self.driver.find_element_by_id("login-form-password").send_keys("autechre0a")
        self.driver.find_element_by_id("login-form-submit").click()
        return Dashboard(self.driver)

class Dashboard(object):
    def __init__(self, driver):
        self.driver = driver
        
    def createIssue(self, driver):
        self.driver.find_element_by_id("create_link").click()
        return CreateIssue(driver)
    
    def searchIssue(self, driver):
        self.driver.find_element_by_id("find_link").click()
        return SearchIssues(driver)

class SearchIssues(object):
    def __init__(self, driver):
        self.driver = driver
    
    def search(self, phrase):
        self.driver.find_element_by_id("quickSearchInput").clear()
        self.driver.find_element_by_id("quickSearchInput").send_keys(phrase+"\n")
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id("issuetable"))
        table = self.driver.find_element_by_id("issuetable")
        body = table.find_element_by_tag_name("tbody")
        rows = body.find_elements_by_class_name("issuerow")
        return rows
    
    def getReporter(self, rows):
        results = []
        for row in rows:
            tags = row.find_elements_by_tag_name("td")
            for tag in tags:
                if tag.get_attribute('class') == 'nav reporter':
                    rr = tag.find_element_by_class_name("user-hover")
                    results.append(rr.get_attribute('rel'))
        return results
        
    def newFilter(self, **kwargs):
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_link_text("New filter"))
        self.driver.find_element_by_link_text("New filter").click()
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_class_name("results-count-start"))
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("searcher-query").is_enabled())
        
        self.driver.find_element_by_id("searcher-query").clear()
        self.driver.find_element_by_id("searcher-query").send_keys(kwargs['phrase'])
        self.driver.find_element_by_css_selector("input.text-submit").click()
        return SearchIssues(self.driver)
     
    def editIssue(self, **kwargs):    
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_link_text(kwargs['sum']))
        self.driver.find_element_by_link_text(kwargs['sum']).click()
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_elements_by_class_name("toggle-title"))
        self.driver.find_element_by_id("edit-issue").click()
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id("description"))
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(kwargs['newdesc'])
        self.driver.find_element_by_id("edit-issue-submit").click()
        WebDriverWait(self.driver, 10).until(lambda driver : kwargs['sum'] in driver.title)
        return Issue(self.driver)

class Issue(object):
    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id("edit-issue"))
        
    def check(self, **kwargs):
        div = self.driver.find_element_by_class_name('user-content-block')
        tag = div.find_element_by_tag_name('p')
        #print tag.text, kwargs['desc']
        return tag.text == kwargs['desc']
        
class CreateIssue(object):
    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("project-field"))
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("issuetype-field"))
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("priority-field"))
        WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("assignee-field"))
        
    def setType(self, itype):
        self.driver.find_element_by_id("issuetype-field").click()
        self.driver.find_element_by_id("issuetype-field").clear()
        self.driver.find_element_by_id("issuetype-field").send_keys(itype)

    def setSummary(self, summary):
        self.driver.find_element_by_id("summary").clear()
        ready = False
        while not ready:
            try:
                WebDriverWait(self.driver, 10).until(lambda driver : driver.find_element_by_id("summary").is_enabled())
            except:
                ready = False
            else:
                ready = True
        self.driver.find_element_by_id("summary").send_keys(summary)

    def setPriority(self, priority):
        self.driver.find_element_by_id("priority-field").click()
        self.driver.find_element_by_id("priority-field").clear()
        self.driver.find_element_by_id("priority-field").send_keys(priority)
    
    def setDescription(self, description):
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(description)
    
    def submit(self):
        self.driver.find_element_by_id("create-issue-submit").click()
        WebDriverWait(self.driver, 10).until(lambda driver : driver.title.lower().startswith("system"))
        return Dashboard(self.driver)
        
     
