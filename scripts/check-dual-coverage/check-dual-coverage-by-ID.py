from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.alert import Alert 

import time
import sys
from datetime import datetime


from dotenv import load_dotenv
from dotenv import dotenv_values


# browser options
use_options = True
stagger = True

# load credentials from .env config
load_dotenv()
env_config = dotenv_values()

share_emp_ID = sys.argv[1]

enrollments = {}
# print("Printing ", share_emp_ID)

# def enterFieldData(field_name, emp_data):
#     global element
#     # global emp_data
#     element = driver.find_element(By.ID, field_name)
#     element.send_keys(emp_data)


class Enrollment:
    def __init__(self, emp_ID="", ssn="", medical=False, dental=False, vision=False, effective_date=None, expiration_date=None):
        self.emp_ID = emp_ID
        self.ssn = ssn
        self.medical = medical
        self.dental = dental
        self.vision = vision
        self.effective_date = effective_date
        self.expiration_date = expiration_date
        self.dependents = []

    def check_date_overlap(self, other_enrollment):
        if not self.effective_date or not self.expiration_date or not other_enrollment.effective_date or not other_enrollment.expiration_date:
            return False  # If any date is missing, no overlap

        # Check if the date ranges overlap
        return (
            self.effective_date <= other_enrollment.expiration_date
            and other_enrollment.effective_date <= self.expiration_date
        )

# Example usage:
# enrollment1 = Enrollment(medical=True, effective_date=datetime(2023, 1, 1), expiration_date=datetime(2023, 12, 31))
# enrollment2 = Enrollment(dental=True, effective_date=datetime(2023, 7, 1), expiration_date=datetime(2024, 6, 30))

# overlap = enrollment1.check_date_overlap(enrollment2)

# print(f"Enrollment 1 and Enrollment 2 {"overlap" if overlap else "do not overlap"}.")

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
    

SHARE_LOGIN_URL = "https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG"
EMP_PERSONAL_DATA_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL"
UPDATE_DEP_BEN_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.DEPEND_BENEF.GBL"

EMP_SSN_HTML_ID = "DERIVED_HR_NID_SPECIAL_CHAR$0"
EMP_SEARCHBOX_HTML_ID ="PERALL_SEC_SRCH_EMPLID"
EFF_DATE_HTML_ID = "NAMES_EFFDT$0"
PERSONAL_PROFILE_TAB_HTML_ID = "ICTAB_2"

if use_options:
  
    # Configure Driver
    print("Configure Driver")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    # chrome_options.add_argument("--kiosk-printing")
    # chrome_options.add_argument("--debug-print")
    # chrome_options.add_argument("--disable-print-preview")
    # chrome_options.add_argument("--use-system-default-printer")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")

    # chrome_options.add_experimental_option("detach", True)   # Theoretically keeps the tab open after script runs. usually crashed by then.
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Configured")

else :
    # open new tab
    driver = webdriver.Chrome()

try:
  # login
    driver.implicitly_wait(2)
    driver.switch_to.new_window("tab")

    # {{{{{{{1}}}}}}} login to SHARE
    print("Login to SHARE")
    driver.get(SHARE_LOGIN_URL)
    # if stagger: time.sleep(2)

    enterFieldData("userid", env_config["SHARE_LOGIN"])
    enterFieldData("pwd", env_config["SHARE_PWD"])

    element.send_keys("\n")
    
    # [[[[[[2]]]]]] personal data
    driver.get(EMP_PERSONAL_DATA_URL)
    if stagger: time.sleep(2)
    element = driver.find_element(By.ID, EMP_SEARCHBOX_HTML_ID)
    element.send_keys(share_emp_ID)
    element.send_keys("\n")

    if stagger: time.sleep(2)

    # emp ssn
    element = driver.find_element(By.ID, EMP_SSN_HTML_ID)
    emp_ssn = element.get_attribute("innerHTML")

    # emp effecitve date
    date_string = driver.find_element(By.ID, EFF_DATE_HTML_ID).get_attribute("innerHTML")
    date_format = "%m/%d/%Y"

    eff_date = datetime.strptime(date_string, date_format)
    exp_date = datetime.strptime("12/31/2999", date_format)

    enrollments[emp_ssn] = Enrollment(share_emp_ID, emp_ssn, False, False, False, eff_date, exp_date)

    # [[[[[[3]]]]]] SHARE dependents 

    # look up dependants of ssn
    dep_ssn = []

    driver.get(UPDATE_DEP_BEN_URL)
    element.send_keys("\n")

    driver.find_element(By.ID, PERSONAL_PROFILE_TAB_HTML_ID).click()

    ix = 0
    dep_ssn_html_id = "DERIVED_HR_NID_SPECIAL_CHAR${ix}".format(ix=ix)
    while driver.find_element(By.ID, dep_ssn_html_id).is_displayed :
        dep_ssn.append(driver.find_element(By.ID, dep_ssn_html_id).get_attribute("value"))
        ix = ix + 1
        dep_ssn_html_id = "DERIVED_HR_NID_SPECIAL_CHAR${ix}".format(ix=ix)
    
    enrollments[share_emp_ID].dependents = dep_ssn
    
    # [[[[[3.1]]]]] dependents SSN

    # Check if DEPS are EMPS
    ## Bool for checked or not.
    ### Recall this function.

    # Check if EMP is EMP & DEP

    # 


finally:  
    # Close all tabs and windows except for the initial one (the first window)
    # for window_handle in driver.window_handles:
    #     if window_handle != driver.current_window_handle:
    #         driver.switch_to.window(window_handle)
    #         driver.close()

    # # Switch back to the initial window (if it"s not already active)
    # if len(driver.window_handles) > 0:
    #     driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.quit()
    chrome_options.quit()