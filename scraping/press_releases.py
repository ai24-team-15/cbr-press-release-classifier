import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Firefox()
driver.get("https://cbr.ru/")

wait = WebDriverWait(driver, 10)

el = driver.find_element(By.CSS_SELECTOR, 'a.tab[data-tabs-tab="4"]')
driver.execute_script("arguments[0].click();", el)

print(el.text) 

time.sleep(2)

btns = driver.find_elements(By.ID, "_buttonLoadNextEvt")

for el in btns:
    print(el.text)


driver.execute_script("arguments[0].click();", btns[1])
print(btns[1].text)







