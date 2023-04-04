import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


driver = webdriver.Chrome()

links = []  # List for add all links
page_index = 1  # Number of page if we have pagination object

while page_index != 3:  # Works until the moment, where number of page will reach the last page
    driver.get(
        f'https://goszakup.gov.kz/ru/search/announce?filter%5Bname%5D=%D0%BF%D1%81%D0%B4&search=&filter%5Bcustomer%5D=&filter%5Bnumber%5D=&filter%5Byear%5D=0&filter%5Bstatus%5D%5B%5D=350&filter%5Bmethod%5D%5B%5D=188&filter%5Bamount_from%5D=&filter%5Bamount_to%5D=&filter%5Btrade_type%5D=&filter%5Bstart_date_from%5D=&filter%5Bstart_date_to%5D=&filter%5Bend_date_from%5D=&filter%5Bend_date_to%5D=&filter%5Bitog_date_from%5D=&filter%5Bitog_date_to%5D=&page={page_index}')
    driver.implicitly_wait(10)

    tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-result"]/tbody')))  # parent object of 50 submission object
    rows = tbody.find_elements(By.TAG_NAME, "tr")  # has 50 submission object
    for row in rows:
        link = row.find_element(By.TAG_NAME, "a").get_attribute("href")  # searches for an object `a` by traversing each submission object
        links.append(link)

    last_page = driver.find_element(By.CSS_SELECTOR,
                                    '#main-wrapper > div.content-block > div.row > div > div:nth-child(4) > div.panel-body > div.row > div.col-md-6.text-center > nav > ul > li:nth-child(8) > a').text
    page_index += 1

    if page_index == int(last_page) + 1:
        page_index = 0
        break

for link in links:
    driver.get(link)
    driver.implicitly_wait(10)
    count_submissions = int(driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div.panel.panel-default > div.panel-footer > div > div:nth-child(1) > p').text[-1])
    deadline_start = driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div.panel.panel-default > div.panel-body > div.row > div:nth-child(2) > div:nth-child(1) > div > input').get_attribute('value')

    if count_submissions < 5:
        continue

    driver.find_element(By.XPATH, '//*[@href="?tab=protocols"]').click()
    id_protocol = driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div:nth-child(8) > div > div > div > div > div > div > div.panel-body > table > tbody > tr:nth-child(2) > td:nth-child(1)').text
    driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div:nth-child(8) > div > div > div > div > div > div > div.panel-body > table > tbody > tr:nth-child(2) > td:nth-child(3) > a').click()

    downloads_folder = os.path.abspath(os.path.join(os.path.expanduser("~"), "Downloads"))
    # get the latest downloaded file in the Downloads folder (assuming it's a .html file)
    time.sleep(5)
    latest_file = max([os.path.join(downloads_folder, f) for f in os.listdir(downloads_folder) if f.endswith('.html')],
                      key=os.path.getctime)

    # open the latest downloaded file in the browser
    driver.get('file:///' + latest_file)
    time.sleep(5)
    text = driver.find_elements(By.TAG_NAME, 'p')[-1]
    execu = f'''
    let scr = document.createElement("input");
    scr.type = "text";
    scr.value = "{deadline_start}"
    '''

    try:
        d = driver.execute_async_script(execu)
    except Exception as e:
        print(str(e))

    time.sleep(5)