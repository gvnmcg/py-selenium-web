from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

print(f"Name of the script      : {sys.argv[0]=}")
print(f"Arguments of the script  1: {sys.argv[1]}")
print(f"Arguments of the script  2: {int(sys.argv[2]) + 1}")

# driver = webdriver.Edge()

# driver.get('https://bing.com')
# driver.switch_to.new_window('tab')


# element = driver.find_element(By.ID, 'sb_form_q')
# element.send_keys('WebDriver')
# element.submit()

time.sleep(5)
# driver.quit()
