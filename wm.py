import requests
import json
from bs4 import BeautifulSoup
import sys


def scrap_detail(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    data = soup.select('#dtlbk-infobk table tr')

    isbn = None
    for i in data:
        detail = i.select('td')
        row = detail[0].text
        if row == 'Pengarang 1':
            print('Penulis : ' + detail[2].text)
        elif row == 'ISBN-10':
            isbn = detail[2].text
        elif row == 'Deskripsi':
            deskripsi = str(detail[2])
            deskripsi = "".join(line.strip() for line in deskripsi.split("\n"))
            temp = deskripsi.split('<br/>')
            penerbit = temp[0][16:]
            print('Penerbit : ' + penerbit.split(',')[0])
            print('Tahun Terbit : ' + penerbit.split(',')[1][1:])
            print('Lokasi Terbit : ' + temp[1])
        elif row == 'Bahasa':
            print('Bahasa : ' + detail[2].text)

    if isbn == None:
        print('ISBN : -')
    else:
        print('ISBN : ' + isbn)


def scrap(name):
    url = "http://katalog.wima.ac.id/result.php?kategori=title&jenis=1&vkriteria=" + name
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    list_book = soup.select('div#hsl-block')

    print("Jumlah Buku : " + str(len(list_book)))
    for i in list_book:
        soup2 = BeautifulSoup(str(i), 'lxml')
        data = soup2.select('div#infobk a')[0]
        print(data['href'])

        title = data.text
        print('Judul : ' + title)
        scrap_detail('http://katalog.wima.ac.id/' + data['href'])
        print('-----------------------------------')


keyword = sys.argv[1]
scrap(keyword)
# scrap_detail('http://katalog.wima.ac.id/detail.php?id=79408&keepThis=true&TB_iframe=true&height=500&width=620')
