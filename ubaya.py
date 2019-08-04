import requests
import json
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
import sys
import mysql.connector
import urllib.request

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dummy_buku"
)


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


def scrap_detail(title, url, category):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    jenis = soup.select('.contentContainer table td')[0].select('span')[0].text
    if(jenis == 'Lihat Detail Buku'):
        data = soup.select('table')[4]

        details = data.select('tr')

        pengarang = details[2].select('td')[2].select('a')[0].text
        penerbit = details[3].select('td')[2].text
        penerbit = "".join(line.strip() for line in penerbit.split("\n"))
        isbn = details[5].select('td')[2].text
        isbn = "".join(line.strip() for line in isbn.split("\n"))
        if isbn == '':
            isbn = '-'

        temp = penerbit.split(':')

        print('Pengarang : ' + pengarang)
        print('Penerbit : ' + temp[1].split(',')[0][1:])
        print('Lokasi Terbit : ' + temp[0])
        print('Tahun Terbit : ' + temp[1].split(',')[1][1:])
        print('ISBN : ' + isbn)
        print('Bahasa : Indonesia')

        insert_id = save_db(title, pengarang, temp[1].split(',')[0][1:], temp[1].split(
            ',')[1][1:], temp[0], isbn, 'Indonesia', category, '2')
        url_image = soup.select('#imgfoto')[0]['src']

        # cek thumbnail buku
        try:
            request = requests.head(url_image)
            save_thumbnail(url_image, str(insert_id))
            print("Thumbnail : YES")
        except Exception as e:
            print("Thumbnail : NO")
    else:
        print('Bukan Buku')


def scrap(name, category, page_now=1):
    name = name.replace(' ', '%20')
    url = 'http://digilib.ubaya.ac.id/index.php?page=list_search&kdbahasa=ID&key=' + \
        name+'&pages=' + str(page_now)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    data = soup.select('#contents_new')[0].select('table')[1]
    list_book = data.select('table')

    print("Pages : " + str(page_now))

    # List Book
    for i in list_book:
        title = i.select('td')[0].text
        title = "".join(line.strip() for line in title.split("\n"))
        print('Title : ' + title)

        # Detail Book
        link_detail = str(i.select('td')[0].select('a')[0]['href'])
        scrap_detail(title, link_detail, category)
        print('----------------------------------------')

    pagination = data.select('tr')[-1].select('a')
    # current page doesn't have element <a>
    for i in pagination:

        link = 'http://digilib.ubaya.ac.id/index.php' + i['href']
        parsed = parse_qs(urlparse(link).query)['pages']
        pages = int(parsed[0])

        if page_now + 1 == pages:
            scrap(link, category, pages)


keyword = sys.argv[1]
category = sys.argv[2]
scrap(keyword, category)
