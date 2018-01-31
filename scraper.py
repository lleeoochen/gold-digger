from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

chrome_driver = './chromedriver'
catalog_url = 'https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx'

browser = webdriver.Chrome(executable_path=chrome_driver)
browser.get(catalog_url)

# Collect all subject names
subject_list = []
subject_html = Select(browser.find_element_by_id('ctl00_pageContent_courseList'))
for option in subject_html.options:
	subject_list.append(option.get_attribute("value"))

# Click through subjects
for subject in subject_list:
	subject_html = Select(browser.find_element_by_id('ctl00_pageContent_courseList'))
	subject_html.select_by_value(subject)
	submit = browser.find_element_by_id('ctl00_pageContent_searchButton')
	submit.click()

	# Collect data
	file = open("output/" + subject + ".html", "w")
	file.write(browser.find_element_by_tag_name('center').get_attribute('innerHTML').encode('utf-8'))
