from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import sys
import mysql.connector
import urllib.request

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="dummy_buku"
# )


def save_db(title, penulis, penerbit, tahun_terbit, lokasi_terbit, isbn, bahasa, category, id_perpustakaan):
     # INSERT DB
    mycursor = mydb.cursor()

    sql = "INSERT INTO book (judul, penulis, penerbit, tahun_terbit, lokasi_terbit, isbn, bahasa, kategori, perpustakaan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (title.upper(), penulis.upper(), penerbit.upper(),
           tahun_terbit, lokasi_terbit.upper(), isbn, bahasa.upper(), category.upper(), id_perpustakaan)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.lastrowid


def save_thumbnail(url, id):
    urllib.request.urlretrieve(
        url, "thumbnail/" + str(id) + ".jpg")


def scrap(category, browser, page_now=1, count_book=0):
    print("--- [ PAGE " + str(page_now) + ' ] ---')

    # wait jquery finised
    try:
        WebDriverWait(browser, 5).until(
            lambda browser: browser.execute_script('return jQuery.active') == 0)
    except TimeoutException:
        print("Timed out waiting for page to load")

    delay = 0.5
    # open modal every book
    count = browser.find_elements_by_css_selector('div > .thumbnail > #hover')
    for i in count:
        i.click()
        count_book += 1
        time.sleep(delay)
        button_close_modal = browser.find_element_by_xpath(
            "//*[@id='myModal']/div/div/div/button")

        # show modal and get detail information of book
        button_close_modal.click()
        soup = BeautifulSoup(browser.page_source, 'lxml')
        data = soup.select('div .isiModal div')
        judul = data[0].text
        penulis = str(str(data[1].text).split('|', 1)[0])[0:-1]
        data_penerbit = str(data[2].text).split('|')
        penerbit = data_penerbit[0][9:-1]
        lokasi_terbit = data_penerbit[1][1:-1]
        tahun_terbit = data_penerbit[2][1:]
        isbn = str(data[3].text).split('|')
        bahasa = data[4].text.split('|')
        url_image = soup.select('#hover img')[0]['src']

        print('Buku ke - ' + str(count_book))
        print('Judul : ' + judul)
        print('Penulis : ' + penulis)
        print('Penerbit : ' + penerbit)
        print('Lokasi Terbit : ' + lokasi_terbit)
        print('Tahun Terbit : ' + tahun_terbit)
        print('ISBN : ' + isbn[1][6:])
        print('Bahasa : ' + bahasa[0][7:])
        print("Image : " + url_image)
        print()

        # insert_id = save_db(judul, penulis, penerbit, tahun_terbit,
        #                     lokasi_terbit, isbn[1][6:], bahasa[0][7:], category, "3")
        # if url_image != 'http://perpustakaan.stts.edu/public/img/cover/buku/noImage.png':
        #     save_thumbnail(url_image, str(insert_id))

        time.sleep(delay)

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
        scrap(category, browser, int(chosen.text), count_book)
        print()


pencarian = sys.argv[1].replace('+', ' ')
category = sys.argv[2]

browser = webdriver.Chrome(
    executable_path=r'C:\Users\MSI-PC\Downloads\chromedriver_win32\chromedriver.exe')

browser.get("http://perpustakaan.stts.edu/index.php/FrontEnd/cari")

keyword = browser.find_element_by_css_selector('input.txCari')
keyword.send_keys(pencarian, Keys.RETURN)

scrap(category, browser)
browser.quit()
