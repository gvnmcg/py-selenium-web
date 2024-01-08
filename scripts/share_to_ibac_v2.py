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

# load credentials

# load_dotenv()
load_dotenv()
config = dotenv_values()

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
    driver = webdriver.Edge()

try:
  # login
        
    # 1 login to SHARE
    print("login to SHARE")
    driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')

    element = driver.find_element(By.ID, 'userid')
    element.send_keys(config['SHARE_LOGIN'])

    element = driver.find_element(By.ID, 'pwd')
    element.send_keys(config['SHARE_PWD'])

    element.send_keys("\n")
    if stagger: time.sleep(2)




    # 2 Employee Serach Form
    print("Employee Serach Form")

    # driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL')
    driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL')
    # driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL?PortalActualURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL&PortalContentURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Modify%20a%20Person&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsp%2fhprd%2f&PortalURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes')
    # element = driver.find_element(By.ID, 'win0divPERALL_SEC_SRCH_EMPLID')
    if stagger: time.sleep(2)
    element = driver.find_element(By.ID, 'PERALL_SEC_SRCH_EMPLID')
    # element.send_keys(config['TEST_SHARE_ID'])
    element.send_keys(share_emp_ID)

    # element = driver.find_element(By.ID, '#ICSearch').click()
    # element.submit()
    element.send_keys("\n")

    if stagger: time.sleep(2)




    # 3 Copy employee personal data into Dictionary
    print("Personal Data")
    emp_data = {}


    # emp_data["eff"] = input("enter effective date: ")
    emp_data["eff"] = config["EFF_DATE"]
  
    # emp_data["rcd"] = input("enter receipt date: ")
    emp_data["rcd"] = input("enter receipt date: ")

    # emp_data["scd"] = input("enter scan date: ")
    emp_data["scd"] = config["SC_DATE"]

    # emp_data["bc"] = input("enter barcode: ")
    emp_data["bc"] = input("enter barcode: ")




    #ssn
    element = driver.find_element(By.ID, 'DERIVED_HR_NID_SPECIAL_CHAR$0')
    emp_data["ssn"] = element.get_attribute('innerHTML')
    # birthdate
    element = driver.find_element(By.ID, 'PERSON_BIRTHDATE')
    emp_data["bd"] = element.get_attribute('innerHTML')
    # effective date
    element = driver.find_element(By.ID, 'NAMES_EFFDT$0')
    emp_data["eff"] = element.get_attribute('innerHTML')

    element = driver.find_element(By.ID, "PERSON_EMPLID")
    emp_data["empid"] = element.get_attribute('innerHTML')

    element = driver.find_element(By.ID, "NAMES_NAME_DISPLAY$0")
    name = element.get_attribute("innerHTML")
    nameArr = name.split()
    emp_data["fn"] = nameArr[0]
    emp_data["ln"] = nameArr[1]

    print(emp_data)



    # 4 Agency Code
    # driver.find_element(By.ID, 'ICTAB_1').click()
    driver.get("https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL?PortalActualURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL&PortalContentURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Job%20Data&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsp%2fhprd%2f&PortalURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes")
    if stagger: time.sleep(2)
    # element = driver.find_element(By.ID, 'PERALL_SEC_SRCH_EMPLID')
    # element.send_keys(config['TEST_SHARE_ID'])
    # element.send_keys("\n")
    # element.submit()
    element = driver.find_element(By.ID, '#ICSearch').click()

    if stagger: time.sleep(4)

    element = driver.find_element(By.ID, 'JOB_BUSINESS_UNIT$0')
    emp_data["bu"] = element.get_attribute('innerHTML')

    # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')
    print(emp_data)




    # 5 Login to IBAC
    print("IBAC")
    driver.switch_to.new_window('tab')
    driver.get("http://ibacweb/RMD2015")

    element = driver.find_element(By.ID, 'partialLogin_userName')
    element.send_keys(config["IBAC_LOGIN"])
    element = driver.find_element(By.ID, 'partialLogin_password')
    element.send_keys(config["IBAC_PASS"])
    element.submit()
    # if stagger: time.sleep(2)


    # 6 Open Employee Vetting Entry

    driver.get("http://ibacweb/RMD2015/StateVetting/StateVetting/SearchStateVetting")
    if stagger: time.sleep(2)
    driver.execute_script("vettingAdd()")
    if stagger: time.sleep(2)




    # Enter Employee Personal Information
    element = driver.find_element(By.ID, "txtEESS")
    element.send_keys(emp_data["ssn"])
    element.send_keys("\n")
    if stagger: time.sleep(2)
    driver.execute_script("addNewEmployee()")

    print(emp_data)

    # 7 submit vett
    if stagger: time.sleep(2)
    element = driver.find_element(By.ID, "txtBirth_F")
    element.send_keys(emp_data["bd"])

    element = driver.find_element(By.ID, "txtEmployID_F")
    element.send_keys(emp_data["empid"])

    element = driver.find_element(By.ID, "txtFirstName_F")
    element.send_keys(emp_data["fn"])

    element = driver.find_element(By.ID, "txtLastName_F")
    element.send_keys(emp_data["ln"])

    if stagger: time.sleep(2)
    # submit button
    # familyEditSubmit()
    driver.execute_script("familyEditSubmit()")
    if stagger: time.sleep(2)
    # driver.find_element(By.TAG_NAME, "body").send_keys("\n")
    alert = Alert(driver) 
    alert.accept()
    # accept alert

    # element = driver.find_element(By.ID, "txtMiddleName_F")
    # element.send_keys(emp_data["mn"])

    # 8 Confirm
    # accept alert
    if stagger: time.sleep(2)

    element = driver.find_element(By.ID, "slDistID_V")
    element.send_keys(emp_data["bu"])

    
    element = driver.find_element(By.ID, "txtHireDate_V")
    element.send_keys(emp_data["eff"])

    
    element = driver.find_element(By.ID, "txtEffectiveDate_V")
    element.send_keys(emp_data["eff"])
    # element.send_keys(emp_data["eff"])

    
    element = driver.find_element(By.ID, "txtReceiptDate_V")
    # element.send_keys(emp_data["bd"])
    element.send_keys(emp_data["rcd"])


    element = driver.find_element(By.ID, "txtScanDate_V")
    # element.send_keys(emp_data["bd"])
    element.send_keys(emp_data["scd"])

    element = driver.find_element(By.ID, "txtBarcode_V")
    # element.send_keys(emp_data["bd"])
    element.send_keys(emp_data["bc"])

    # driver.execute_script("vettingEditSubmit()")


finally:
    driver.quit()



def enterFieldwithData(field_name, emp_data):
    element = driver.find_element(By.ID, field_name)
    element.send_keys(emp_data)