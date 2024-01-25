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

"""Load Credentials""" 
# .env config
load_dotenv("C:\Program Files\Google\Chrome\.env")
env_config = dotenv_values("C:\Program Files\Google\Chrome\.env")
# load_dotenv("test-data\.env")
test_config = dotenv_values("test-data\.env")

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

"""Constants"""
SHARE_LOGIN_PAGE_URL = "https://hcm.share.state.nm.us/psp/hprd/?cmd=login&languageCd=ENG"
SHARE_PERSONAL_INFO_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).PERSONAL_DATA.GBL"
SHARE_JOBDATA_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL"
SHARE_HEALTH_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_BASE_BENEFITS.HEALTH_BENEFITS.GBL"
SHARE_SSN_URL = "https://hcm.share.state.nm.us/psc/hprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).NID_LOOKUP.GBL"

NATIONAL_ID_FIELD_HTML_ID = "DERIVED_HR_NATIONAL_ID"
COV_CHNG_DATE_HTML_ID = "HEALTH_BENEFIT_COVERAGE_BEGIN_DT$0"
BEN_PLAN_HTML_ID = "HEALTH_BENEFIT_BENEFIT_PLAN$0"
EMP_SEARCH_HTML_NAME = "EMPL_BEN_SRCH_EMPLID"
ACTIVE_STATUS_HTML_ID = "JOB_HR_STATUS$0"
SEARCH_FIELD_HTML_ID = 'EMPLMT_SRCH_COR_EMPLID'

IBAC_LOGIN_PAGE_URL =  "http://ibacweb/RMD2015"
IBAC_STATE_INQUIRY_URL = "http://ibacweb/RMD2015/Inquiry/Inquiry/SearchPage"

SEARCHBAR_HTML_ID = "txtSearch"
ENRL_TABLE_HTML_ID = "enrmBody"

"""Browser Config"""
use_options = True
stagger = True
debug = True
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
def enterFieldDataByID(field_name, input_text):
    global element
    # global emp_data
    if stagger: time.sleep(1)
    element = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.ID, field_name))
    )
    element.clear()
    element.send_keys(input_text)

def enterFieldDataByName(field_name, input_text):
    global element
    # global emp_data
    if stagger: time.sleep(1)
    element = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.NAME, field_name))
    )
    element.clear()
    element.send_keys(input_text)

def getDataByID(field_id_name):
    global driver
    # global emp_data
    if stagger: time.sleep(1)
    return WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, field_id_name))
    ).get_attribute('innerHTML')



"""MAIN"""
def login_to_share():
    if debug : print("login to SHARE")

    if driver.current_url != SHARE_LOGIN_PAGE_URL:
        driver.get(SHARE_LOGIN_PAGE_URL)

    enterFieldDataByID('userid', env_config['SHARE_LOGIN'])
    enterFieldDataByID('pwd', env_config['SHARE_PWD'])
    element.send_keys("\n")

    if debug : print("logged in to SHARE")
    return

def find_ID_via_SSN(emp_ssn):
    if debug : print("Get ID")
    if debug : print("SSN: ", emp_ssn)

    if driver.current_url != SHARE_SSN_URL:
        driver.get(SHARE_SSN_URL)

    enterFieldDataByID(NATIONAL_ID_FIELD_HTML_ID,  emp_ssn)
    driver.find_element(By.ID, "DERIVED_HR_LOOKUP_NID_BTN").click()

    emp_ID = getDataByID("NID_SRCH_VW_EMPLID$0")

    if debug: print("Employee ID: ", emp_ID)
    return emp_ID

"""
def find_ID_via_SSN_func(emp_ssn):
    if debug : print("find_ID_via_SSN: ", emp_ssn)
    is_list = []
    enterFieldDataByID(NATIONAL_ID_FIELD_HTML_ID,  emp_ssn)
    driver.find_element(By.ID, "DERIVED_HR_LOOKUP_NID_BTN").click()
    emp_ID = getDataByID("NID_SRCH_VW_EMPLID$0")
    if stagger: time.sleep(1)
    if debug: print("Employee ID: ", emp_ID)
    return emp_ID
"""

def check_job_status(emp_ID): 
    if debug : print("check_job_status: ", emp_ID)
    
    if driver.current_url != SHARE_JOBDATA_URL:
        driver.get(SHARE_JOBDATA_URL)

    if stagger: time.sleep(1)
    if driver.find_element(By.ID, SEARCH_FIELD_HTML_ID).is_displayed():
        enterFieldDataByID(SEARCH_FIELD_HTML_ID, emp_ID)
        element.send_keys("\n")
    else:
        driver.find_element(By.ID, "#ICList").click()
        enterFieldDataByID(SEARCH_FIELD_HTML_ID, emp_ID)
        element.send_keys("\n")
    job_status = getDataByID(ACTIVE_STATUS_HTML_ID)

    if debug: print("Employee Status: ", job_status)
    return job_status

def active_medical_check(emp_ID):
    if debug : print("active_medical_check")

    if driver.current_url != SHARE_HEALTH_URL:
        driver.get(SHARE_HEALTH_URL)

    # Search for Employee and 
    # element = driver.find_element(By.NAME, EMP_SEARCH_HTML_NAME)
    # if element.is_displayed():
    #     element.clear()
    #     element.send_keys(emp_ID)
    #     element.send_keys("\n")
    enterFieldDataByName(EMP_SEARCH_HTML_NAME, emp_ID)
    element.send_keys("\n")

    # get Benefits Carrier
    if stagger: time.sleep(1)
    ben_carrier = getDataByID(BEN_PLAN_HTML_ID)
    print("ben_carrier: ", ben_carrier)

    # active -> check health -> check Carrier & term date
    # if ben_carrier.__contains__("BCBS"):
    if "BCBS" in ben_carrier:
        emp_status = "Active"
    else:
        cov_change_date = getDataByID(COV_CHNG_DATE_HTML_ID)
        emp_status = "Termed " + cov_change_date

    print("Employee Status: ", emp_status)
    return emp_status

def login_IBAC():
    if driver.current_url != IBAC_LOGIN_PAGE_URL:
        driver.get(IBAC_LOGIN_PAGE_URL)
    enterFieldDataByID('partialLogin_userName', env_config["IBAC_LOGIN"])
    enterFieldDataByID('partialLogin_password', env_config["IBAC_PASS"])
    # element.submit()
    element.send_keys("\n")

def inactive_medical_check(ssn):
    if debug : print("inactive_medical_check")

    if driver.current_url != IBAC_STATE_INQUIRY_URL:
        driver.get(IBAC_STATE_INQUIRY_URL)
    
    # incative -> check ibac inquiry -> check cobra -> check expire date
    if stagger: time.sleep(1)
    enterFieldDataByID(SEARCHBAR_HTML_ID, ssn)
    driver.find_element(By.ID, "Button1").click()
    # element.send_keys("\n")
    # load page
    if stagger: time.sleep(5)
    try:
        element = driver.find_element(By.ID, "enrmBody")
        elem_enrl_list = element.find_elements(By.TAG_NAME, "td")

        enrl_type = elem_enrl_list[4].get_attribute("innerHTML")
        eff_date = elem_enrl_list[0].get_attribute("innerHTML")

        print("enrl type:  ", enrl_type)
        if enrl_type  == "Cobra":
            return "Cobra " + eff_date
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
            # incative -> check ibac
            login_IBAC()
            out_status = inactive_medical_check(ssn)
        return out_status
    except:
        return "failed"

emp_map = {}

def term_check_all_func():

    id_set = {}
    df = pd.read_excel(input_file_path, sheet_name="CancelNoMatch", header=3)
    # rows = df.iloc[50:].iterrows()
    rows = df.iterrows()

    ssn_col = "SubSocSec"
    out_term_col = "Term Status"
    out_id_col = "State IDs"
    
    # get IDs from SSN
    for ix, row in rows:
        print("#: ", ix)
        df.at[ix, out_id_col] = find_ID_via_SSN(row[ssn_col])  # Write to the second column
        df.to_excel(output_file_path, index=False)

    # get term status from IDs
    for ix, row in rows:
        print("#: ", ix)
        emp_ID = row[out_id_col]
        emp_ssn = row[ssn_col]  
        if debug : print("emp_ID: ", emp_ID, ", emp_ssn: ", emp_ssn)
        # if debug : print("rows: ", row)

        # if emp_ID == "nan":
        #     emp_ID  = find_ID_via_SSN(row[ssn_col])
        # elif "&nbsp" in emp_ID: 
        #     out_status = inactive_medical_check(emp_ssn)
        
        try:
            emp_status = check_job_status(emp_ID)
            if debug : print("emp_status: ", emp_status)

            if emp_status == "Active":
                out_status = active_medical_check(emp_ID)
            else:
                login_IBAC()
                out_status = inactive_medical_check(emp_ssn)
        except:
            # return out_status
            out_status = "&NBSP error"

        id_set[emp_ID] = out_status

        df.at[ix, out_term_col] = out_status  # Write to the second column
        df.to_excel(output_file_path, index=False)

def test_XLSX():

    df = pd.read_excel(input_file_path, sheet_name="CancelNoMatch", header=3)
    ssn_col = "SubSocSec"

    term_col = "Unnamed: 17"
    id_col   = "Unnamed: 15"

    print("df.head(", df.head())
    print("df.columns)", df.columns)
    print("df[ssn_col]", df[ssn_col])
    # print("df[id_col]", df[id_col])
    # print("df[term_col]", df[term_col])
    print("df", df)

def check_Ibac():
    login_IBAC()
    df = pd.read_excel(input_file_path, sheet_name="CancelNoMatch", header=3)
    # rows = df.iloc[50:].iterrows()
    rows = df.iterrows()

    ssn_col = "SubSocSec"
    in_term_col = "Term Status"
    in_id_col = "State IDs"

    for ix, row in rows:
        emp_term = row[in_term_col]  
        emp_ID = row[in_id_col]
        emp_ssn = row[ssn_col]  

        if "&NBSP" in emp_term:
            print("#: ", ix)
            if debug : print("emp_ID: ", emp_ID, ", emp_ssn: ", emp_ssn)
            out_status = inactive_medical_check(row[ssn_col])

        # try:
        #     out_status = inactive_medical_check(emp_ssn)
        # except:
        #     # return out_status
        #     out_status = "&NBSP error"
            df.at[ix, "term"] = out_status
            df.to_excel(output_file_path, index=False)
    df.close()

def main():
    try:
        login_to_share()
        # test_XLSX()
        # check_Ibac()
        term_check_all_func()
        return
    except Exception as e:
        # By this way we can know about the type of error occurring
            print("The error is: ", e)
            # print(driver.page_source)
            # print(driver.print_page)

    finally : 
        time.sleep(1000)
        driver.quit()

main()



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