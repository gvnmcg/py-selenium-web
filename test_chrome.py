from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()

config = dotenv_values()

path = r"C:\Users\gmcguire.EASI\Downloads\chromedriver_win32\chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
#Change chrome driver path accordingly
chrome_driver = path
driver = webdriver.Chrome(options=chrome_options)
print (driver.current_url)

driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')

element = driver.find_element(By.ID, 'userid')
element.send_keys(config['SHARE_LOGIN'])

element = driver.find_element(By.ID, 'pwd')
element.send_keys(config['SHARE_PWD'])

element.send_keys("\n")


time.sleep(5000)
driver.quit()