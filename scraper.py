from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Setup constants
CHROME_DRIVER = './chromedriver'
CATALOG_URL = 'https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx'
SUBJECT_ID = 'ctl00_pageContent_courseList'
QUARTER_ID = 'ctl00_pageContent_quarterList'
SEARCH_ID = 'ctl00_pageContent_searchButton'


# Collect all subject names
def get_list(browser, element_id):
	newlist = []
	html = Select(browser.find_element_by_id(element_id))
	for option in html.options:
		newlist.append(option.get_attribute("value"))
	return newlist


# Setup selenium
browser = webdriver.Chrome(executable_path=CHROME_DRIVER)
browser.get(CATALOG_URL)

# Get lists
subject_list = get_list(browser, SUBJECT_ID)
quarter_list = get_list(browser, QUARTER_ID)


# Click through subjects
for subject in subject_list:
	for quarter in quarter_list:

		# Select subject, quarter
		Select(browser.find_element_by_id(SUBJECT_ID)).select_by_value(subject)
		Select(browser.find_element_by_id(QUARTER_ID)).select_by_value(quarter)

		# Click on search button
		submit = browser.find_element_by_id(SEARCH_ID)
		submit.click()

		# Collect data
		file = open("output/" + quarter + "_" + subject + ".html", "w")
		file.write(browser.find_element_by_tag_name('center').get_attribute('innerHTML').encode('utf-8'))