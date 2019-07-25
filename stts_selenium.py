from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup


def scrap(browser, page_now=1):
    print("--- [ PAGE " + str(page_now) + ' ] ---')

    # wait jquery finised
    try:
        WebDriverWait(browser, 5).until(
            lambda browser: browser.execute_script('return jQuery.active') == 0)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # open modal every book
    count = browser.find_elements_by_css_selector('div > .thumbnail > #hover')
    for i in count:
        i.click()
        time.sleep(1)
        button_close_modal = browser.find_element_by_xpath(
            "//*[@id='myModal']/div/div/div/button")

        # show modal and get detail information of book
        button_close_modal.click()
        soup = BeautifulSoup(browser.page_source, 'lxml')
        data = soup.select('div .isiModal div')
        judul = data[0].text
        penulis = str(str(data[1].text).split('|', 1)[0])[0:-1]
        data_penerbit = str(data[2].text).split('|')
        penerbit = data_penerbit[0][0:-1]
        lokasi_terbit = data_penerbit[1][1:-1]
        tahun_terbit = data_penerbit[2][1:]
        isbn = str(data[3].text).split('|')

        print('Judul : ' + judul)
        print('Penulis : ' + penulis)
        print('Penerbit : ' + penerbit)
        print('Lokasi Terbit : ' + lokasi_terbit)
        print('Tahun Terbit : ' + tahun_terbit)
        # print('ISBN : ' + (isbn[2])[5])

        time.sleep(1)

    # pagination
    pagination = browser.find_elements_by_css_selector(
        'ul.pagination > li > a')
    chosen = None
    for i in pagination:
        try:
            page = int(i.text)
            if page_now + 1 == page:
                chosen = i
        except Exception as e:
            pass

    if chosen != None:
        chosen.click()
        scrap(browser, int(chosen.text))
        print()


browser = webdriver.Chrome(
    executable_path=r'C:\Users\MSI-PC\Downloads\chromedriver_win32\chromedriver.exe')

browser.get("http://perpustakaan.stts.edu/index.php/FrontEnd/cari")

keyword = browser.find_element_by_css_selector('input.txCari')
keyword.send_keys('android', Keys.RETURN)

scrap(browser)
browser.quit()
