from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv
from dotenv import dotenv_values

import pandas as pd

import time
import sys

# load credentials from .env config
load_dotenv("C:\Program Files\Google\Chrome\.env")
env_config = dotenv_values("C:\Program Files\Google\Chrome\.env")
# load_dotenv("test-data\.env")
test_config = dotenv_values("test-data\.env")

input_file_path = ""
output_file_path = ""
file_path = "executables/term-check/BCBSAcct.xlsx"

# browser options
use_options = True
stagger = True
debug = True

SHARE_LOGIN_PAGE_URL = "https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG"
SHARE_PERSONAL_INFO_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL"
SHARE_JOBDATA_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL"
SHARE_HEALTH_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.HEALTH_BENEFITS.GBL"
SHARE_SSN_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).NID_LOOKUP.GBL"

NATIONAL_ID_FIELD_HTML_ID = "DERIVED_HR_NATIONAL_ID"
COV_CHNG_DATE_HTML_ID = "HEALTH_BENEFIT_COVERAGE_BEGIN_DT$0"
BEN_PLAN_HTML_ID = "HEALTH_BENEFIT_BENEFIT_PLAN$0"
EMP_SEARCH_HTML_ID = "EMPL_BEN_SRCH_EMPLID"
ACTIVE_STATUS_HTML_ID = "JOB_HR_STATUS$0"
SEARCH_FIELD_HTML_ID = 'EMPLMT_SRCH_COR_EMPLID'

IBAC_LOGIN_PAGE_URL =  "http://ibacweb/RMD2015"
IBAC_STATE_INQUIRY_URL = "http://ibacweb/RMD2015/Inquiry/Inquiry/SearchPage"

SEARCHBAR_HTML_ID = "txtSearch"
ENRL_TABLE_HTML_ID = "enrmBody"

global driver
if use_options:
  
    # Configure Driver
    if debug : print("Configure Driver")
    chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
    chrome_options.add_experimental_option("detach", True)   # Theoretically keeps the tab open after script runs. usually crashed by then.
    driver = webdriver.Chrome(options=chrome_options)
    if debug : print("Driver Configured")

else :
    # open new tab
    driver = webdriver.Chrome()


"""UTILITY"""
def enterFieldData(field_name, input_text):
    global element
    # global emp_data
    element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_name))
    )
    element.send_keys(input_text)

def copyDataByID(field_id_name):
    global driver
    # global emp_data
    return WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_id_name))
    ).get_attribute('innerHTML')



"""MAIN"""
def login_to_share():
    if debug : print("login to SHARE")
    driver.get(SHARE_LOGIN_PAGE_URL)
    enterFieldData('userid', env_config['SHARE_LOGIN'])
    enterFieldData('pwd', env_config['SHARE_PWD'])
    element.send_keys("\n")

def find_ID_via_SSN(emp_ssn):
    if debug : print("find_ID_via_SSN: ", emp_ssn)
    driver.get(SHARE_SSN_URL)
    if stagger: time.sleep(1)
    # if driver.find_element(By.ID, NATIONAL_ID_FIELD_HTML_ID).is_displayed():
    driver.find_element(By.ID, NATIONAL_ID_FIELD_HTML_ID).clear()
    enterFieldData(NATIONAL_ID_FIELD_HTML_ID,  emp_ssn)
    driver.find_element(By.ID, "DERIVED_HR_LOOKUP_NID_BTN").click()
    if stagger: time.sleep(1)
    emp_ID = copyDataByID("NID_SRCH_VW_EMPLID$0")
    if debug: print("Employee ID: ", emp_ID)
    return emp_ID

def find_ID_via_SSN_func(emp_ssn):
    if debug : print("find_ID_via_SSN: ", emp_ssn)
    is_list = []
    if stagger: time.sleep(1)
    # if driver.find_element(By.ID, NATIONAL_ID_FIELD_HTML_ID).is_displayed():
    driver.find_element(By.ID, NATIONAL_ID_FIELD_HTML_ID).clear()
    enterFieldData(NATIONAL_ID_FIELD_HTML_ID,  emp_ssn)
    driver.find_element(By.ID, "DERIVED_HR_LOOKUP_NID_BTN").click()
    if stagger: time.sleep(1)
    emp_ID = copyDataByID("NID_SRCH_VW_EMPLID$0")
    if stagger: time.sleep(1)
    if debug: print("Employee ID: ", emp_ID)
    return emp_ID


def check_job_status(emp_ID): 
    if debug : print("check_job_status: ", emp_ID)
    driver.get(SHARE_JOBDATA_URL)
    if stagger: time.sleep(1)
    if driver.find_element(By.ID, SEARCH_FIELD_HTML_ID).is_displayed():
        driver.find_element(By.ID, SEARCH_FIELD_HTML_ID).clear()
        enterFieldData(SEARCH_FIELD_HTML_ID, emp_ID)
        element.send_keys("\n")
    else:
        driver.find_element(By.ID, "#ICList").click()
        driver.find_element(By.ID, SEARCH_FIELD_HTML_ID).clear()
        enterFieldData(SEARCH_FIELD_HTML_ID, emp_ID)
        element.send_keys("\n")
    if stagger: time.sleep(1)
    job_status = copyDataByID(ACTIVE_STATUS_HTML_ID)
    if debug: print("Employee Status: ", job_status)
    return job_status

def active_medical_check(emp_ID):
    if debug : print("active_medical_check")
    # active -> check health -> check Carrier & term date
    if stagger: time.sleep(1)
    driver.get(SHARE_HEALTH_URL)
    element = driver.find_element(By.NAME, EMP_SEARCH_HTML_ID)
    if element.is_displayed():
        element.clear()
        element.send_keys(emp_ID)
        element.send_keys("\n")
    if stagger: time.sleep(1)
    ben_plan = copyDataByID(BEN_PLAN_HTML_ID)
    print("ben_plan: ", ben_plan)
    if ben_plan.__contains__("BCBS"):
        emp_status = "Active"
    else:
        cov_change_date = copyDataByID(COV_CHNG_DATE_HTML_ID)
        emp_status = "Termed " + cov_change_date
    if stagger: time.sleep(2)
    print("Employee Status: ", emp_status)
    return emp_status

def login_IBAC():
    driver.get(IBAC_LOGIN_PAGE_URL)
    enterFieldData('partialLogin_userName', env_config["IBAC_LOGIN"])
    enterFieldData('partialLogin_password', env_config["IBAC_PASS"])
    element.submit()

def inactive_medical_check(ssn):
    if debug : print("inactive_medical_check")
    # incative -> check ibac inquiry -> check cobra -> check expire date
    login_IBAC()
    driver.get(IBAC_STATE_INQUIRY_URL)
    if stagger: time.sleep(1)
    enterFieldData(SEARCHBAR_HTML_ID, ssn)
    driver.find_element(By.ID, "Button1").click()
    # element.send_keys("\n")
    if stagger: time.sleep(5)
    try:
        element = driver.find_element(By.ID, "enrmBody")
        print( element)
        # print(element.find_elements(By.TAG_NAME, "td"))
        elem_enrl_list = element.find_elements(By.TAG_NAME, "td")
        enrl_type = elem_enrl_list[4].get_attribute("innerHTML")
        print("enrl type:  ", enrl_type)
        if enrl_type  == "Cobra":
            return "Cobra " + elem_enrl_list[0].get_attribute("innerHTML")
        else:
            return elem_enrl_list.__str__()
    except:
        return "Not in IBAC"

"""Routines"""
def single_term_check(ssn):
    try:
        if debug : print("single_term_check: ", ssn)
        emp_ID = find_ID_via_SSN(ssn)
        if debug : print("ID: ", emp_ID)
        emp_status = check_job_status(emp_ID)
        if debug : print("line_status: ", emp_status)
        if emp_status == "Active":
            out_status = active_medical_check(emp_ID)
        else:
            # raise Exception('go to IBAC')
            out_status = inactive_medical_check(ssn)
        return out_status
    except:
        return "failed"

def single_file_term_check_file():
   
    # with open(input_file_path, 'r', encoding='utf-8') as input_file, 
    #         open(output_file_path, 'w', encoding='utf-8') as output_file:
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')
    for line_ssn in input_file:
        print(line_ssn)
        out_line = single_term_check(line_ssn)
        output_file.write(line_ssn.strip() + ": " + out_line + "\n")

    input_file.close()
    output_file.close()
emp_map = {}

def single_file_term_check_XLSX():
    file_path = ""

    df = pd.read_excel(file_path, sheet_name="CancelNoMatch", header=3)
    in_col = "SubSocSec"
    term_col = "Unnamed: 13"
    id_col = "Unnamed: 15"
    print(df[in_col])
    # ssn_list = df["Unnamed: 3"].tolist()
    # for ix in range(3, len(ssn_list)+3):
    #     # if line_ssn.is_digit() and len(line_ssn) == 9:
    #     print(ssn_list[ix])
    #     out_line = single_term_check(ssn_list[ix])
    #     df.at[ix, 'Unnamed: 15'] = out_line
    #     df.at[ix, 'Unnamed: 16'] = ssn_list[ix]
    #     df.to_excel(out_file_path, index=False)

emp_map = {}
"""
class Emp():
    def __init__(self, ssn) -> None:
        self.ssn = ssn

    def __str__(self) -> str:
        return ""  + self.ssn + " " + self.share_id


def page_wise_term_check_file():
    input_file_path = ""
    output_file_path = ""
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        #Map SSN  Map
        for line_ssn in input_file:
            emp_map[line_ssn] = Emp(line_ssn)
        print(emp_map)
        driver.get(SHARE_SSN_URL)
        # add Employee ID to Map
        for line_ssn in emp_map.keys():
            share_id = find_ID_via_SSN(line_ssn)
            emp_map[line_ssn].share_id = share_id
            print("SHARE ID, SSN ", line_ssn, share_id)
        # Check Each Job Data
        for line_ssn in emp_map.keys():
            job_status = check_job_status(emp_map[line_ssn].share_id)
            emp_map[line_ssn].job_status = job_status
            print("SHARE ID, SSN ", line_ssn, share_id)
        # If active Check Each Health
        for line_ssn in emp_map.keys():
            job_status = active_medical_check(job_status)
            emp_map[line_ssn].job_status = job_status
            print("SHARE ID, SSN ", line_ssn, share_id)
        # Output to File
        for line_ssn in emp_map.keys():
            output_file.write(emp_map[line_ssn] + "\n")
"""

def term_check_all_func():
    df = pd.read_excel(file_path, sheet_name="CancelNoMatch", header=3)
    ssn_col = "SubSocSec"
    term_col = "Unnamed: 17"
    id_col = "Unnamed: 15"
    # driver.get(SHARE_SSN_URL)
    driver.get(SHARE_JOBDATA_URL)

    # df[id_col] = df[in_col].apply(find_ID_via_SSN_func)
    # for emp_ssn in df[in_col]:
    for ix, row in df.iloc[70:].iterrows():
        emp_ID = row[id_col]  # Process data from the first column
        emp_ssn = row[ssn_col]  # Process data from the first column
        try:
            emp_status = check_job_status(emp_ID)

            if debug : print("emp_status: ", emp_status)
            if debug : print("emp_ID: ", emp_ID)
            if debug : print("emp_ssn: ", emp_ssn)

            if emp_status == "Active":
                out_status = active_medical_check(emp_ID)
            else:
                # raise Exception('go to IBAC')
                out_status = inactive_medical_check(emp_ssn)
        except:
            # return out_status
            out_status = "&NBSP error"

        df.at[ix, term_col] = out_status  # Write to the second column
        df.to_excel(out_file_path, index=False)

def main():
    try:
        login_to_share()
        # single_file_term_check_XLSX()
        term_check_all_func()
        return
        # single_file_term_check_file()
        # return 
        print(sys.argv)
        if len(sys.argv) == 2:
            print(single_term_check(sys.argv[1]))
        # if len(sys.argv) == 3:
        #     print(single_term_check(sys.argv[1]))
        else:
            page_wise_term_check_file()
    except Exception as e:
        # By this way we can know about the type of error occurring
            print("The error is: ", e)
            # print(driver.page_source)
            # print(driver.print_page)

    finally : 
        time.sleep(1000)
        driver.quit()

main()
