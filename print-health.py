from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from dotenv import load_dotenv
from dotenv import dotenv_values

# load creds
load_dotenv()

# browser options
use_options = true

if use_options:
    # use open tab
    options = webdriver.EdgeOptions()
    options.add_experimental_option('debuggerAddress', dotenv_values("EDGE_HOST_POST"))
    driver = webdriver.Edge(options=options)
else :
    # open new tab
    driver = webdriver.Edge()

try:
    # login
    driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')
    # time.sleep(5000)

    element = driver.find_element(By.ID, 'userid')
    element.send_keys(dotenv_values('SHARE_LOGIN'))

    element = driver.find_element(By.ID, 'pwd')
    element.send_keys(dotenv_values('SHARE_PWD'))

    element.submit()

    # print health, given the ID has been entered
    driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.HEALTH_BENEFITS.GBL')
    driver.find_element(By.ID, "#ICSearch").click()
    driver.find_element(By.ID, "$ICField7$hviewall$0").click()
    driver.print_page()
    # driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.LIFE_ADD_BENEF.GBL')
    # driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.DISABILITY_BENEFIT.GBL')
    # driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.FSA_BENEFITS.GBL')

    time.sleep(5000)
finally:
    driver.quit()


def login():
    driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')
    time.sleep(5000)

    element = driver.find_element(By.ID, 'userid')
    element.send_keys(dotenv_values('SHARE_LOGIN'))

    element = driver.find_element(By.ID, 'pwd')
    element.send_keys(dotenv_values('SHARE_PWD'))

    element.submit()
    