import requests
import json
from bs4 import BeautifulSoup
import sys
import general


def scrap_detail(url, title):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    data = soup.select('#dtlbk-infobk table tr')

    print('Judul : ' + title)
    isbn = '-'
    penulis = '-'
    penerbit = '-'
    tahun_terbit = '-'
    lokasi_terbit = '-'
    bahasa = '-'
    new_ddc = None

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
        elif row == 'DDC':
            ddc = detail[2].text
            temp = ddc.split(' ')

            index = None
            for idx, text in enumerate(temp):
                for i in text:
                    if i.isalpha():
                        index = idx
                        break
                if index != None:
                    break
            if index != None:
                if len(temp) > 1 and index == 0:
                    new_ddc = temp[1]
                elif index > 0:
                    new_ddc = temp[0]
            else:
                new_ddc = temp[0]

    url_image = soup.select('#dtlbk-cover img')[0]['src']
    # print('URL Image : ' + url_image)
    print('ISBN : ' + isbn)
    print('DDC : ' + ('-' if new_ddc == None else new_ddc))

    # INSERT DB
    insert_id = general.save_db(
        title, penulis, penerbit, tahun_terbit, lokasi_terbit, isbn, bahasa, "1", new_ddc)
    if url_image != 'images/noimage-big.gif':
        general.save_thumbnail(url_image, str(insert_id))


def scrap(name):
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
                     data['href'], title)
        print()


keyword = sys.argv[1]
scrap(keyword)
# scrap_detail('http://katalog.wima.ac.id/detail.php?id=79408&keepThis=true&TB_iframe=true&height=500&width=620')
