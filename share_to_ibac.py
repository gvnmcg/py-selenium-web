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

finally:
    driver.quit()