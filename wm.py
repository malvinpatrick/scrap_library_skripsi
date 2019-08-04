import requests
import json
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


def scrap_detail(url, title, category):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    data = soup.select('#dtlbk-infobk table tr')

    print('Judul : ' + title)
    isbn = '-'
    penulis = '-'
    penerbit = '-'
    tahun_terbit = '-'
    lokasi_terbit = '-'
    bahasa = 'Indonesia'

    for i in data:
        detail = i.select('td')
        row = detail[0].text
        if row == 'Pengarang 1':
            penulis = detail[2].text
            print('Penulis : ' + detail[2].text)
        elif row == 'ISBN-10':
            isbn = detail[2].text
        elif row == 'Deskripsi':
            deskripsi = str(detail[2])
            deskripsi = "".join(line.strip() for line in deskripsi.split("\n"))
            temp = deskripsi.split('<br/>')
            tpenerbit = temp[0][16:]

            penerbit = tpenerbit.split(',')[0]
            tahun_terbit = tpenerbit.split(',')[1][1:]
            lokasi_terbit = temp[1]

            print('Penerbit : ' + penerbit)
            print('Tahun Terbit : ' + tahun_terbit)
            print('Lokasi Terbit : ' + lokasi_terbit)
        elif row == 'Bahasa':
            bahasa = detail[2].text
            print('Bahasa : ' + bahasa)

    url_image = soup.select('#dtlbk-cover img')[0]['src']
    print('URL Image : ' + url_image)
    print('ISBN : ' + isbn)

    # INSERT DB
    insert_id = save_db(title, penulis, penerbit, tahun_terbit,
                        lokasi_terbit, isbn, bahasa, category, "1")
    if url_image != 'images/noimage-big.gif':
        save_thumbnail(url_image, str(insert_id))


def scrap(name, category):
    url = "http://katalog.wima.ac.id/result.php?kategori=title&jenis=1&vkriteria=" + name
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    list_book = soup.select('div#hsl-block')

    print("Jumlah Buku : " + str(len(list_book)))
    for index, i in enumerate(list_book):
        soup2 = BeautifulSoup(str(i), 'lxml')
        data = soup2.select('div#infobk a')[0]
        print('Buku ke-' + str(index))
        title = data.text
        scrap_detail('http://katalog.wima.ac.id/' +
                     data['href'], title, category)
        print()


keyword = sys.argv[1]
category = sys.argv[2]
scrap(keyword, category)
# scrap_detail('http://katalog.wima.ac.id/detail.php?id=79408&keepThis=true&TB_iframe=true&height=500&width=620')
