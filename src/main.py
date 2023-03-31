from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
links = []
page_index = 1

while page_index != 0:
    driver.get(
        f'https://goszakup.gov.kz/ru/search/announce?filter%5Bname%5D=%D0%BF%D1%81%D0%B4&search=&filter%5Bcustomer%5D=&filter%5Bnumber%5D=&filter%5Byear%5D=0&filter%5Bstatus%5D%5B%5D=350&filter%5Bmethod%5D%5B%5D=188&filter%5Bamount_from%5D=&filter%5Bamount_to%5D=&filter%5Btrade_type%5D=&filter%5Bstart_date_from%5D=&filter%5Bstart_date_to%5D=&filter%5Bend_date_from%5D=&filter%5Bend_date_to%5D=&filter%5Bitog_date_from%5D=&filter%5Bitog_date_to%5D=&page={page_index}')
    driver.implicitly_wait(5)

    tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-result"]/tbody')))
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
        links.append(link)

    last_page = driver.find_element(By.CSS_SELECTOR,
                                    '#main-wrapper > div.content-block > div.row > div > div:nth-child(4) > div.panel-body > div.row > div.col-md-6.text-center > nav > ul > li:nth-child(8) > a').text
    page_index += 1

    if page_index == int(last_page) + 1:
        page_index = 0
        break
driver.quit()