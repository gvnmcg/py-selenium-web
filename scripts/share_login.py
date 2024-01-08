from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()

config = dotenv_values()

driver = webdriver.Chrome()

driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')

element = driver.find_element(By.ID, 'userid')
element.send_keys(config['SHARE_LOGIN'])

element = driver.find_element(By.ID, 'pwd')
element.send_keys(config['SHARE_PWD'])

element.send_keys("\n")

time.sleep(5000)
driver.quit()