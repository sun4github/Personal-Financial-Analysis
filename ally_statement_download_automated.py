# Download the ally transactions for current month, from the 1st
# till todays date
# 2018-02-05 SK: Good as of today. likely to change once ally updates their interface

import datetime
import time
import random
from selenium import webdriver

import get_download_folders as wFolders

#Custom Private Information -- DO NOT SHARE
YOUR_ALLY_USERNAME = ''
YOUR_ALLY_PW = ''

# to use a custom profile
# settings can be found in about:config
ally_firefox_profile = webdriver.firefox.firefox_profile.FirefoxProfile();

localDirectory = wFolders.get_download_path()

def set_firefox_download_preferences():
    ally_firefox_profile.set_preference("browser.download.folderList",1);
    ally_firefox_profile.set_preference("browser.download.manager.showWhenStarting",False);
    ally_firefox_profile.set_preference("browser.download.dir",localDirectory)
    ally_firefox_profile.set_preference("browser.helperApps.alwaysAsk.force",False);
    ally_firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv;")

def download_this_month_csv():

    set_firefox_download_preferences()
    
    #launch firefox browser instance
    browser=webdriver.firefox.webdriver.WebDriver(firefox_profile=ally_firefox_profile)

    #send to a url
    browser.get('https://www.ally.com/')

    #select the login type
    login_type=webdriver.support.select.Select(browser.find_element_by_css_selector('#account'))
    login_type.select_by_visible_text('Bank or Invest Login')

    #username
    username_elem = browser.find_element_by_css_selector('#username')
    username_elem.send_keys(YOUR_ALLY_USERNAME)

    #password
    
    password_elem = browser.find_element_by_css_selector('#password')
    password_elem.send_keys(YOUR_ALLY_PW)

    password_elem.submit()

    time.sleep(random.randint(15,20))



    #select checking account
    checking_elem = browser.find_element_by_css_selector('#ember1749')
    checking_elem.click()

    time.sleep(random.randint(7,15))

    #click download
    download_elem = browser.find_element_by_css_selector('a.filter-button-wrapper:nth-child(1)')
    download_elem.click()
    
    time.sleep(random.randint(4,8))

    #select file format
    file_format_elem = webdriver.support.select.Select(browser.find_element_by_css_selector('#select-file-format'))
    file_format_elem.select_by_visible_text('CSV')

    #select date range
    date_range_elem = webdriver.support.select.Select(browser.find_element_by_css_selector('#select-date-range'))
    date_range_elem.select_by_visible_text('Custom Dates')

    todays_date = datetime.datetime.today()

    first_day_of_month = todays_date.strftime('%b') + ' 01, ' + todays_date.strftime('%Y')

    date_until = todays_date.strftime('%b %d, %Y')

    #start date format: Feb 05, 2018 
    #downloadStartDate
    start_date_range = browser.find_element_by_css_selector('#downloadStartDate')
    start_date_range.send_keys(first_day_of_month)

    #downloadEndDate
    end_date_range = browser.find_element_by_css_selector('#downloadEndDate')
    end_date_range.send_keys(date_until)

    time.sleep(random.randint(4,8))


    #click download
    end_date_range.submit()

    #ember3778 or #ember3777
    #elem = browser.find_element_by_css_selector('#ember3777')
    #elem.click()

    time.sleep(random.randint(5,15))

    #click logout
    elem=browser.find_element_by_css_selector('a.is-hidden-mobile:nth-child(3)')
    elem.click()

    time.sleep(random.randint(2,5))

    #close browser
    browser.quit()



