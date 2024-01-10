import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 

import time
from selenium.webdriver.chrome.options import Options
import sys


from dotenv import load_dotenv
from dotenv import dotenv_values

emp_data = {}

def enterFieldData(field_name, emp_data):
    global element
    # global emp_data
    element = driver.find_element(By.ID, field_name)
    element.send_keys(emp_data)

def copyEmployeeDataByID(field_id_name, emp_data_key):
    global element
    global emp_data
    element = driver.find_element(By.ID, field_id_name)
    emp_data[emp_data_key] = element.get_attribute('innerHTML')


# load credentials from .env config
load_dotenv()
env_config = dotenv_values()

share_emp_ID = sys.argv[1]

# browser options
use_options = True

if use_options:
  
    # Configure Driver
    print("Configure Driver")
    stagger = True
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    # chrome_options.add_experimental_option("detach", True)   # Theoretically keeps the tab open after script runs. usually crashed by then.
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver Configured")


else :
    # open new tab
    driver = webdriver.Chrome()

try:
  # login
   

    # 1 login to SHARE
    print("login to SHARE")
    driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')

    enterFieldData('userid', env_config['SHARE_LOGIN'])
    enterFieldData('pwd', env_config['SHARE_PWD'])

    element.send_keys("\n")
    if stagger: time.sleep(2)

    # 2 Employee Serach Form
    print("Employee Serach Form")

    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL')
    if stagger: time.sleep(2)

    enterFieldData('PERALL_SEC_SRCH_EMPLID', share_emp_ID)

    element.send_keys("\n")

    if stagger: time.sleep(2)


    # 3 Copy employee personal data into Dictionary
    print("Personal Data")

    emp_data["eff"] = env_config["EFF_DATE"]
    emp_data["hd"] = env_config["EFF_DATE"]
    emp_data["scd"] = env_config["SC_DATE"]
    emp_data["bc"] = input("enter barcode: ")
    emp_data["rcd"] = datetime.today.strftime('%m/%d/%Y')


    #ssn
    copyEmployeeDataByID('DERIVED_HR_NID_SPECIAL_CHAR$0', "ssn")
    # birthdate
    copyEmployeeDataByID('PERSON_BIRTHDATE', "bd")
    # effective date
    copyEmployeeDataByID('NAMES_EFFDT$0', "eff")
    # employee id
    copyEmployeeDataByID("PERSON_EMPLID", "empid")

    element = driver.find_element(By.ID, "NAMES_NAME_DISPLAY$0")
    name = element.get_attribute("innerHTML")
    nameArr = name.split()
    emp_data["fn"] = nameArr[0]
    emp_data["ln"] = nameArr[1]

    print(emp_data)



    # 4 Agency Code
    driver.get("https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL?PortalActualURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL&PortalContentURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Job%20Data&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsp%2fhprd%2f&PortalURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes")
    if stagger: time.sleep(2)
 
    element = driver.find_element(By.ID, '#ICSearch').click()

    if stagger: time.sleep(4)

    # element = driver.find_element(By.ID, 'JOB_BUSINESS_UNIT$0')
    # emp_data["bu"] = element.get_attribute('innerHTML')
    copyEmployeeDataByID('JOB_BUSINESS_UNIT$0',"bu")

    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')
    print(emp_data)

    # 5 Login to IBAC
    print("IBAC")
    driver.switch_to.new_window('tab')
    driver.get("http://ibacweb/RMD2015")

    enterFieldData( 'partialLogin_userName', env_config["IBAC_LOGIN"])
    enterFieldData( 'partialLogin_password', env_config["IBAC_PASS"])
    element.submit()
    # if stagger: time.sleep(2)

    # 6 Open Employee Vetting Entry
    driver.get("http://ibacweb/RMD2015/StateVetting/StateVetting/SearchStateVetting")
    if stagger: time.sleep(2)
    driver.execute_script("vettingAdd()")
    if stagger: time.sleep(2)


    # Enter Employee Personal Information
    # element = driver.find_element(By.ID, )
    # element.send_keys(emp_data["ssn"])
    enterFieldData("txtEESS", emp_data["ssn"])
    
    element.send_keys("\n")
    if stagger: time.sleep(2)
    driver.execute_script("addNewEmployee()")

    print(emp_data)

    # 7 submit vett
    if stagger: time.sleep(2)
    enterFieldData("txtBirth_F", emp_data["bd"])
    enterFieldData("txtEmployID_F", emp_data["empid"])
    enterFieldData("txtFirstName_F", emp_data["fn"])
    enterFieldData("txtLastName_F", emp_data["ln"])

    if stagger: time.sleep(2)
    
    # submit button
    driver.execute_script("familyEditSubmit()")
    if stagger: time.sleep(2)
    
    # accept alert
    alert = Alert(driver) 
    alert.accept()

    # 8 Confirm
    # accept alert
    if stagger: time.sleep(2)
    enterFieldData("slDistID_V", emp_data["bu"])
    enterFieldData("txtHireDate_V", emp_data["hd"])
    enterFieldData("txtEffectiveDate_V", emp_data["eff"])
    enterFieldData("txtReceiptDate_V",emp_data["rcd"])
    enterFieldData("txtScanDate_V", emp_data["scd"])
    enterFieldData("txtBarcode_V",emp_data["bc"])

finally:
    driver.quit()

