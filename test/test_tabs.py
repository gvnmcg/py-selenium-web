from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import sys


from dotenv import load_dotenv
from dotenv import dotenv_values

# load credentials

# load_dotenv()
load_dotenv()
config = dotenv_values()

# share_emp_ID = sys.argv[1]

# browser options
use_options = True

if use_options:
  
    # Configure Driver
    print("Configure Driver")
    stagger = True
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    # chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Configured")

    driver.switch_to.new_window('tab')


