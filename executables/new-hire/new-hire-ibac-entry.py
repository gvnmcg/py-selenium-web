from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv
from dotenv import dotenv_values

import datetime
import time
import sys

emp_data = {}

# load credentials from .env config
load_dotenv("C:\Program Files\Google\Chrome\.env")
env_config = dotenv_values("C:\Program Files\Google\Chrome\.env")

# browser options
use_options = True
stagger = False
debug = False

def enterFieldData(field_name, emp_data):
    global element
    # global emp_data
    element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_name))
    )
    element.send_keys(emp_data)

def copyEmployeeDataByID(field_id_name, emp_data_key):
    global element
    global emp_data
    # global emp_data
    element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_id_name))
    )
    emp_data[emp_data_key] = element.get_attribute('innerHTML')


# def enterFieldData(field_name, emp_data):
#     global element
#     # global emp_data
#     element = driver.find_element(By.ID, field_name)
#     element.send_keys(emp_data)

# def copyEmployeeDataByID(field_id_name, emp_data_key):
#     global element
#     global emp_data
#     element = driver.find_element(By.ID, field_id_name)
#     emp_data[emp_data_key] = element.get_attribute('innerHTML')
    
SHARE_LOGIN_PAGE_URL = "https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG"
SHARE_PERSONAL_INFO_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL"
SHARE_JOBDATA_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL"

IBAC_LOGIN_PAGE_URL =  "http://ibacweb/RMD2015"
IBAC_STATE_ENTRY_URL = "http://ibacweb/RMD2015/StateVetting/StateVetting/SearchStateVetting"

BARCODE_KEY = "bc"

EMP_SHARE_ID_KEY = "empID"
EMP_SSN_KEY = "ssn"

EMP_SCAN_DATE_KEY = "scd"
EMP_RECP_DATE_KEY = "rcd" 
EMP_BIRTH_DATE_KEY = "bd" 
EMP_EFF_DATE_KEY = "eff" 
EMP_HIRE_DATE_KEY = "hd" 
EMP_JOB_CODE_KEY = "bu" 

EMP_FIRST_NAME_KEY = "fn" 
EMP_LAST_NAME_KEY = "ln" 


share_emp_ID = input("Enter Employee SHARE ID: ")
emp_data[BARCODE_KEY] = input("enter barcode: ")

# share_emp_ID = sys.argv[1]
# emp_data[BARCODE_KEY] = sys.argv[2]


if use_options:
  
    # Configure Driver
    if debug : print("Configure Driver")
    chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    chrome_options.add_experimental_option("detach", True)   # Theoretically keeps the tab open after script runs. usually crashed by then.
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    if debug : print("Driver Configured")


else :
    # open new tab
    driver = webdriver.Chrome()

try:
  # login
   
    # 1 login to SHARE
    if debug : print("login to SHARE")
    driver.get(SHARE_LOGIN_PAGE_URL)

    enterFieldData('userid', env_config['SHARE_LOGIN'])
    enterFieldData('pwd', env_config['SHARE_PWD'])
    element.send_keys("\n")

    # 2 Employee Serach Form
    if debug : print("Employee Serach Form")
    driver.get(SHARE_PERSONAL_INFO_URL)
    if stagger: time.sleep(1)

    enterFieldData('PERALL_SEC_SRCH_EMPLID', share_emp_ID)
    element.send_keys("\n")
    if stagger: time.sleep(1)

    # 3 Copy employee personal data into Dictionary
    if debug : print("Personal Data")

    emp_data["scd"] = datetime.date.today().strftime('%m/%d/%Y')
    emp_data["rcd"] = datetime.date.today().strftime('%m/%d/%Y')

    #ssn
    copyEmployeeDataByID('DERIVED_HR_NID_SPECIAL_CHAR$0', EMP_SSN_KEY)
    # birthdate
    copyEmployeeDataByID('PERSON_BIRTHDATE', EMP_BIRTH_DATE_KEY)
    # effective date
    copyEmployeeDataByID('NAMES_EFFDT$0', EMP_EFF_DATE_KEY)
    # hire date
    copyEmployeeDataByID('NAMES_EFFDT$0', EMP_HIRE_DATE_KEY)
    # employee id
    copyEmployeeDataByID("PERSON_EMPLID", EMP_SHARE_ID_KEY)

    element = driver.find_element(By.ID, "NAMES_NAME_DISPLAY$0")
    name = element.get_attribute("innerHTML")
    nameArr = name.split()
    emp_data[EMP_FIRST_NAME_KEY] = nameArr[0]
    emp_data[EMP_LAST_NAME_KEY] = nameArr[1]

    if debug : print(emp_data)



    # 4 Agency Code
    driver.get(SHARE_JOBDATA_URL)
    if stagger: time.sleep(2)
 
    element = driver.find_element(By.ID, '#ICSearch').click()

    if stagger: time.sleep(4)

    copyEmployeeDataByID('JOB_BUSINESS_UNIT$0',EMP_JOB_CODE_KEY)

    if debug : print(emp_data)

    # 5 Login to IBAC
    if debug : print("IBAC")
    driver.switch_to.new_window('tab')
    driver.get(IBAC_LOGIN_PAGE_URL)

    enterFieldData( 'partialLogin_userName', env_config["IBAC_LOGIN"])
    enterFieldData( 'partialLogin_password', env_config["IBAC_PASS"])
    element.submit()
    # if stagger: time.sleep(2)

    # 6 Open Employee Vetting Entry
    driver.get(IBAC_STATE_ENTRY_URL)
    if stagger: time.sleep(2)
    driver.execute_script("vettingAdd()")
    if stagger: time.sleep(2)


    # Enter Employee Personal Information
    enterFieldData("txtEESS", emp_data[EMP_SSN_KEY])
    
    element.send_keys("\n")
    if stagger: time.sleep(2)
    driver.execute_script("addNewEmployee()")

    if debug : print(emp_data)
    if stagger: time.sleep(1)

    # 7 submit vett
    # if not driver.find_element(By.ID, "vettingDiv").is_displayed:
    if stagger: time.sleep(2)
    enterFieldData("txtBirth_F", emp_data[EMP_BIRTH_DATE_KEY])
    enterFieldData("txtEmployID_F", emp_data[EMP_SHARE_ID_KEY])
    enterFieldData("txtFirstName_F", emp_data[EMP_FIRST_NAME_KEY])
    enterFieldData("txtLastName_F", emp_data[EMP_LAST_NAME_KEY])
    if stagger: time.sleep(2)

    # submit button
    driver.execute_script("familyEditSubmit()")
    if stagger: time.sleep(2)

    # accept alert
    stagger: time.sleep(2)
    alert = Alert(driver) 
    alert.accept()

    # 8 Confirm
    # accept alert
    # if driver.find_element(By.ID, "vettingDiv").is_displayed:
    if stagger: time.sleep(2)
    enterFieldData("slDistID_V", emp_data[EMP_JOB_CODE_KEY])
    enterFieldData("txtHireDate_V", emp_data[EMP_HIRE_DATE_KEY])
    enterFieldData("txtEffectiveDate_V", emp_data[EMP_EFF_DATE_KEY])
    enterFieldData("txtReceiptDate_V",emp_data[EMP_RECP_DATE_KEY])
    enterFieldData("txtScanDate_V", emp_data[EMP_SCAN_DATE_KEY])
    enterFieldData("txtBarcode_V",emp_data[BARCODE_KEY])

    driver.execute_script("alert('Please Verify and click Submit');")

except:
    if debug : print("An error occured, Please finish manually.")

finally:
    if debug : print("Closing.")
    # Open another website in a new tab
    # driver.execute_script("window.open('https://google.com', '_blank');")

    # Detach the second tab and switch back to the first tab
    # driver.switch_to.window(driver.window_handles[0])
    # driver.quit()

