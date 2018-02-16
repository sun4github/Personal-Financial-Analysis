# Download the discover credit card transactions for current month, from the 1st
# till todays date
# 2018-02-05 SK: Good as of today. likely to change once discover updates their interface


#download and update path to geckodriver.exe location (after pip install selenium)
#C:\Users\skanuri\Documents\My Python\geckodriver-v0.19.1-win64

#selenium web driver documentation
#http://www.seleniumhq.org/docs/03_webdriver.jsp#introducing-webdriver
#http://selenium-python.readthedocs.io/api.html

from selenium import webdriver
import time
import datetime
import random

import get_download_folders as wFolders

#Custom Private Information -- DO NOT SHARE
YOUR_DISCOVER_USERNAME = ''
YOUR_DISCOVER_PW = ''

# to use a custom profile
# settings can be found in about:config
firefoxProfile=webdriver.firefox.firefox_profile.FirefoxProfile();

localDirectory = wFolders.get_download_path()

def set_firefox_download_preferences():
    firefoxProfile.set_preference("browser.download.folderList",1);
    firefoxProfile.set_preference("browser.download.manager.showWhenStarting",False)
    firefoxProfile.set_preference("browser.download.dir",localDirectory)
    firefoxProfile.set_preference("browser.helperApps.alwaysAsk.force",False);
    firefoxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/csv;")

def download_this_month_csv():
    set_firefox_download_preferences()
    
    browser=webdriver.firefox.webdriver.WebDriver(firefox_profile=firefoxProfile) 


    #send browser to a url
    browser.get('https://discover.com/')
    
    #find element and enter text
    uid_elem = browser.find_element_by_css_selector('#userid-content')
    uid_elem.send_keys(YOUR_DISCOVER_USERNAME)
    pw_elem = browser.find_element_by_css_selector('#password-content')
    pw_elem.send_keys(YOUR_DISCOVER_PW)

    #use the form submit
    pw_elem.submit()

    #now introduce delay, for the other page to load
    time.sleep(random.randint(10,20)) # 30 seconds delay

    # now click on "view all activity"
    vallact_elem = browser.find_element_by_css_selector('#pending-view-act')
    vallact_elem.click()

    #now introduce delay, for the other page to load
    time.sleep(random.randint(5,10)) # 10 seconds delay


    # now click on "Change Date"
    cdate_elem = browser.find_element_by_css_selector('#date-tab')
    cdate_elem.click()


    todays_date = datetime.datetime.today()

    first_day_of_month = todays_date.strftime('%m') + '/01/' + todays_date.strftime('%Y')

    date_until = todays_date.strftime('%m/%d/%Y')

    #now enter from date

    cdate_start_elem = browser.find_element_by_css_selector('#calendar-inputStart')
    cdate_start_elem.send_keys(first_day_of_month)

    #now enter to date

    cdate_end_elem = browser.find_element_by_css_selector('#calendar-inputEnd')
    cdate_end_elem.send_keys(date_until)

    #now click go

    cdate_go_elem = browser.find_element_by_css_selector('#calGobtnlnk')
    cdate_go_elem.click()

    #wait 10 secs
    time.sleep(random.randint(5,10))

    #click on "Download" button
    download_elem = browser.find_element_by_css_selector('#search-download-button')
    download_elem.click()

    #wait 5 secs for modal
    time.sleep(random.randint(3,8))

    #click on "CSV" image in modal
    chose_csv_elem = browser.find_element_by_css_selector('#search-download-options-csv > img:nth-child(1)')
    chose_csv_elem.click()

    time.sleep(random.randint(2,4))

    #click on "download" button in modal
    download_csv_elem = browser.find_element_by_css_selector('.download-overlay-button')
    download_csv_elem.click()


    #wait 10 secs
    time.sleep(random.randint(7,15))

    #now logout
    logout_elem = browser.find_element_by_css_selector('a.log-out-link:nth-child(1)')
    logout_elem.click()

    #move browser to the previous page
    #browser.back()

    #move browser to the next page
    #browser.forward()

    #refresh browser page
    #browser.refresh()

    time.sleep(random.randint(2,5))

    #now close the browser
    browser.quit()

#main area
#download_this_month_csv()
