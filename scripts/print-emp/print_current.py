from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.alert import Alert 

import time
from selenium.webdriver.chrome.options import Options
import sys


from dotenv import load_dotenv
from dotenv import dotenv_values


# browser options
use_options = True
stagger = True

# load credentials from .env config
load_dotenv()
env_config = dotenv_values()

share_emp_ID = sys.argv[1]
print("Printing ", share_emp_ID)

# def enterFieldData(field_name, emp_data):
#     global element
#     # global emp_data
#     element = driver.find_element(By.ID, field_name)
#     element.send_keys(emp_data)

def enterFieldData(field_name, emp_data):
    global element
    # global emp_data
    element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_name))
    )
    # element = driver.find_element(By.ID, "$ICField7$hviewall$0")
    # if element : element.click()
    # element = driver.find_element(By.ID, field_name)
    element.send_keys(emp_data)

def click_view_all_onload(elem_id):
    #print
    if stagger: time.sleep(1)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, elem_id))
        )
        if element : element.click()
    except: 
        # element = driver.find_element(By.ID, elem_id)
        print("no view all")
    


if use_options:
  
    # Configure Driver
    print("Configure Driver")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    # chrome_options.add_argument('--kiosk-printing')
    # chrome_options.add_argument('--debug-print')
    # chrome_options.add_argument('--disable-print-preview')
    # chrome_options.add_argument('--use-system-default-printer')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # chrome_options.add_experimental_option("detach", True)   # Theoretically keeps the tab open after script runs. usually crashed by then.
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Configured")

else :
    # open new tab
    driver = webdriver.Chrome()

try:
  # login
    driver.implicitly_wait(2)
    driver.switch_to.new_window('tab')



    # 1 login to SHARE
    print("Login to SHARE")
    driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')
    # if stagger: time.sleep(2)

    enterFieldData('userid', env_config['SHARE_LOGIN'])
    enterFieldData('pwd', env_config['SHARE_PWD'])

    element.send_keys("\n")

    # [[[2]]] print Health, Life, Disability, and FSA

    #health
    print("Printing Health")
    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.HEALTH_BENEFITS.GBL?')
    # if stagger: time.sleep(1)

    # serach employee once
    enterFieldData('EMPL_BEN_SRCH_EMPLID', share_emp_ID)
    element.send_keys("\n")

    #print
    view_all_id = "$ICField7$hviewall$0"
    click_view_all_onload(view_all_id)
    if stagger: time.sleep(1)
    driver.execute_script('window.print();')

    #life
    print("Printing Life")
    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.LIFE_ADD_BENEF.GBL')

    #print
    view_all_id = "PLAN_TYPE$hviewall$0"
    click_view_all_onload(view_all_id)
    if stagger: time.sleep(1)
    driver.execute_script('window.print();')

    # Disability
    print("Printing Diability")
    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.DISABILITY_BENEFIT.GBL')

    #print
    view_all_id = "$ICField6$hviewall$0"
    click_view_all_onload(view_all_id)
    if stagger: time.sleep(1)
    driver.execute_script('window.print();')

    # Spending
    print("Printing Spending")
    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.FSA_BENEFITS.GBL')
    
    view_all_id = "$ICField6$hviewall$0"
    click_view_all_onload(view_all_id)
    if stagger: time.sleep(1)
    driver.execute_script('window.print();')

finally:  
    # Close all tabs and windows except for the initial one (the first window)
    # for window_handle in driver.window_handles:
    #     if window_handle != driver.current_window_handle:
    #         driver.switch_to.window(window_handle)
    #         driver.close()

    # # Switch back to the initial window (if it's not already active)
    # if len(driver.window_handles) > 0:
    #     driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.quit()
    chrome_options.quit()