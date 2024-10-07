import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import httpx
import pandas as pd


driver = webdriver.Firefox()
driver.get("https://www.cbr.ru/dkp/mp_dec/")

wait = WebDriverWait(driver, 10)
content = driver.find_element(By.ID, "tab_content_t1")
btn = content.find_element(By.TAG_NAME, "button")

while btn:
    btn.click()
    time.sleep(2)
    content = driver.find_element(By.ID, "tab_content_t1")
    
    try:
        btn = content.find_element(By.TAG_NAME, "button")
    except NoSuchElementException:
        btn = None

data = []
releases = content.find_elements(By.CLASS_NAME, "previews_day")
for item in releases:

    data_item = []
    date = item.find_element(By.CLASS_NAME, "previews_day-date")
    link = item.find_element(By.TAG_NAME, "a")

    data_item.append(date.text)
    data_item.append(link.get_attribute('href'))
    data_item.append(link.text)
    data.append(data_item)

for i, (_, link, _) in enumerate(data):
    response = httpx.get(link)
    tree = BeautifulSoup(response.text, 'html.parser')

    release = tree.find_all('div', {'class' : 'landing-text'})[0]
    data[i].append(release.text)
    time.sleep(1)

df = pd.DataFrame(data, columns=['date', 'link', 'title', 'release'])
df.to_csv('mp_dec.csv', index=False)

time.sleep(5)
driver.quit()

