from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.alert import Alert 

import time
import datetime
import sys
import subprocess
# import sys


from dotenv import load_dotenv
from dotenv import dotenv_values


subprocess.call("chrome.exe -remote-debugging-port=9014 --profile-directory=ERISA", shell=True)

# browser options
use_options = True
stagger = True

# load credentials from .env config
load_dotenv()
env_config = dotenv_values()

# share_emp_ID = sys.argv[1]
# print("Printing ", share_emp_ID)

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
    driver.get("https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_AUTOMATED_BENEFITS.BAS_PARTIC_PRC.GBL")
    driver.find_element(By.ID, "BAS_PAR_PRC_KEY_BAS_EVENT_CHG").click()
    driver.find_element(By.ID, "BAS_PAR_PRC_KEY_EVENT_CLASS").send_keys("OE")
    driver.find_element(By.ID, "BAS_PAR_PRC_KEY_EVENT_STATUS").send_keys("C")
    driver.find_element(By.ID, "BAS_PAR_PRC_KEY_SCHED_ID").send_keys("OE24")
    # driver.find_element(By.TAG_NAME, "body").send_keys("\n")
    
    if stagger: time.sleep(2)
    driver.find_element(By.ID, "BAS_PAR_PRC_KEY_BAS_SELECT_DATA").click()
    if stagger: time.sleep(2)

    driver.find_element(By.ID, "$ICField2$hviewall$0").click()

    # copy each ID
    emp_IDs = []
    next_page_button_ID = "$ICField2$hdown$0"
    emp_ID_elem_ID = "BAS_PARTIC_EMPLID${ix}"

    try: 
        # while next page is available
        while driver.find_element(By.ID, next_page_button_ID).is_displayed() :
            for ix in range(99): 
                # emp_ID_str = emp_ID_elem_ID.format(ix=ix) 
                emp_IDs.append(driver.find_element(By.ID, emp_ID_elem_ID.format(ix=ix)).get_attribute("innerHTML"))
            driver.find_element(By.ID, next_page_button_ID).click()
            if stagger: time.sleep(2)

        
        # last page
        for ix in range(99): 
            # emp_ID_str = emp_ID_elem_ID.format(ix=ix) 
            emp_IDs.append(driver.find_element(By.ID, emp_ID_elem_ID.format(ix=ix)).get_attribute("innerHTML"))
        print(emp_IDs)

        f = open(datetime.date.today().__str__() + "_Event_out_of_Sequence.txt", "x")
        for emp_ID in emp_IDs:
            print(emp_ID, file=f)
        sys.stdout = f
        f.close()
        
    except:
        print(emp_IDs)


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
    # chrome_options.quit()