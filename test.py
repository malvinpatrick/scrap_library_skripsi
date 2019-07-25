from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome(
    executable_path=r'C:\Users\MSI-PC\Downloads\chromedriver_win32\chromedriver.exe')

browser.get("https://github.com/TheDancerCodes")
# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//img[@class='avatar width-full height-full rounded-2']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# find_elements_by_xpath returns an array of selenium objects.
titles_element = browser.find_elements_by_xpath(
    "//span[@class='repo js-pinnable-item']")
# use list comprehension to get the actual repo titles and not the selenium objects.
titles = [x.text for x in titles_element]
# print out all the titles.
print('titles:')
print(titles, '\n')
