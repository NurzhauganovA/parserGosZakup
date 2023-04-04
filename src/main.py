import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
count_entries = 0


def getAllLinks():
    global count_entries
    # Function that will return containing all links of submissions
    links = []
    # Number of page if we have pagination object
    page_index = 1

    # Works until the moment, where number of page will reach the last page
    while page_index != 0:
        driver.get(
            f'https://goszakup.gov.kz/ru/search/announce?filter%5Bname%5D=%D0%BF%D1%81%D0%B4&search=&filter%5Bcustomer%5D=&filter%5Bnumber%5D=&filter%5Byear%5D=0&filter%5Bstatus%5D%5B%5D=350&filter%5Bmethod%5D%5B%5D=188&filter%5Bamount_from%5D=&filter%5Bamount_to%5D=&filter%5Btrade_type%5D=&filter%5Bstart_date_from%5D=&filter%5Bstart_date_to%5D=&filter%5Bend_date_from%5D=&filter%5Bend_date_to%5D=&filter%5Bitog_date_from%5D=&filter%5Bitog_date_to%5D=&page={page_index}')
        driver.implicitly_wait(10)

        # Count of entries
        count_entries = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#main-wrapper > div.content-block > div.row > div > div:nth-child(4) > div.panel-heading > div > div > div > small > strong')))
        count_entries = int(count_entries.text.split()[-2])

        # Parent object of 50 submission object
        tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="search-result"]/tbody')))
        # Has 50 submission object
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            # Searches for an object `a` by traversing each submission object
            href = row.find_element(By.TAG_NAME, "a").get_attribute(
                "href")
            links.append(href)

        # Get last page of pagination block
        last_page = driver.find_element(By.CSS_SELECTOR,
                                        '#main-wrapper > div.content-block > div.row > div > div:nth-child(4) > div.panel-body > div.row > div.col-md-6.text-center > nav > ul > li:nth-child(8) > a').text
        # By adding +1 for page bypass all pagination pages
        page_index += 1

        if page_index == int(last_page) + 1:
            # If reaches the last page, then loop will stop
            page_index = 0
            break
    assert count_entries == len(links), 'getAllLinks() function is True!'
    return links


def checkTrigger():
    # Function that will work out the main actions of triggers
    for link in getAllLinks():
        driver.get(link)
        driver.implicitly_wait(10)

        # Get count of submissions
        count_submissions = int(driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div.panel.panel-default > div.panel-footer > div > div:nth-child(1) > p').text[-1])
        # Get the value of the accepting submissions deadline
        deadline_start = driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div.panel.panel-default > div.panel-body > div.row > div:nth-child(2) > div:nth-child(1) > div > input').get_attribute('value')

        # Check first trigger
        if count_submissions < 5:
            continue

        # Find the element of the object protocols
        driver.find_element(By.XPATH, '//*[@href="?tab=protocols"]').click()
        # Find the element of the object protocols
        driver.find_element(By.CSS_SELECTOR, '#main-wrapper > div.content-block > div:nth-child(8) > div > div > div > div > div > div > div.panel-body > table > tbody > tr:nth-child(2) > td:nth-child(3) > a').click()

        # Passing the directory <Downloads> from disk as argument
        downloads_folder = os.path.abspath(os.path.join(os.path.expanduser("~"), "Downloads"))
        # Get the latest downloaded file in the Downloads folder (assuming it's a .html file)
        time.sleep(5)
        # Looks for the last file that ends in <.html>
        latest_file = max([os.path.join(downloads_folder, f) for f in os.listdir(downloads_folder) if f.endswith('.html')],
                          key=os.path.getctime)

        # Open the latest downloaded file in the browser
        driver.get('file:///' + latest_file)
        time.sleep(5)
        # Takes a value on the created <input> element
        execu = f'''
        let scr = document.createElement("input");
        scr.type = "text";
        scr.value = "{deadline_start}"
        '''
        driver.execute_async_script(execu)


if __name__ == '__main__':
    checkTrigger()