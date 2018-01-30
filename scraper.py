from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

chrome_driver = './chromedriver'
catalog_url = 'https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx'

browser = webdriver.Chrome(executable_path=chrome_driver)
browser.get(catalog_url)

subjects = Select(browser.find_element_by_name('ctl00$pageContent$courseList'))
options = subjects.options

for option in options:
	subjects.select_by_value(option.get_attribute("value"))