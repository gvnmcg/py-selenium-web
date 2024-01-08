from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


from dotenv import load_dotenv
from dotenv import dotenv_values

# Configure Driver
load_dotenv()
config = dotenv_values()
stagger = True
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
driver = webdriver.Chrome(options=chrome_options)

# login to SHARE
driver.get('https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG')

element = driver.find_element(By.ID, 'userid')
element.send_keys(config['SHARE_LOGIN'])

element = driver.find_element(By.ID, 'pwd')
element.send_keys(config['SHARE_PWD'])

element.send_keys("\n")
if stagger: time.sleep(2)

# Employee Serach Form

# driver.get('https://hcm.share.state.nm.us/psp/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL')
driver.get('https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL?PortalActualURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL&PortalContentURL=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2fEMPLOYEE%2fHRMS%2fc%2fADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Modify%20a%20Person&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsp%2fhprd%2f&PortalURI=https%3a%2f%2fhcm.share.state.nm.us%2fpsc%2fhprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes')
# element = driver.find_element(By.ID, 'win0divPERALL_SEC_SRCH_EMPLID')
element = driver.find_element(By.ID, 'PERALL_SEC_SRCH_EMPLID')
element.send_keys(config['TEST_SHARE_ID'])
element.send_keys("\n")

if stagger: time.sleep(2)

# Compy employee personal data into Dictionary
emp_data = {}
element = driver.find_element(By.ID, 'DERIVED_HR_NID_SPECIAL_CHAR$0')
emp_data["ssn"] = element.get_attribute('innerHTML')

driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')

# Login to IBAC
driver.get("http://ibacweb/RMD2015")

element = driver.find_element(By.ID, 'partialLogin_userName')
element.send_keys(config["IBAC_LOGIN"])
element = driver.find_element(By.ID, 'partialLogin_password')
element.send_keys(config["IBAC_PASS"])
element.submit()
# if stagger: time.sleep(2)

# Open Employee Vetting Entry
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

if stagger: time.sleep(4)
driver.quit()