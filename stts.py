import requests
import json
from bs4 import BeautifulSoup
import importlib
import sys
import general


def scrap(s, name, page=1, count=0, url='http://perpustakaan.stts.edu/index.php/FrontEnd/cariAjax'):
    print("URL : " + url)
    if page > 1:
        param = {
            'page': page
        }
        print("param :"+str(param))
        books = s.get(url=url, params=param)
    else:
        data = {
            'cb[]': 'judul',
            'submit': 'true',
            'dataCari': name,
            'jenis': 'Buku',
            'filterRb': 'cari',
        }
        print('data = ' + str(data))
        books = s.post(url, data=data)

    source = books.text
    result = json.loads(source)['hasil']

    for i in result:
        count = count+1
        print("BUKU KE-" + str(count))
        judul = i['buku_judul']
        penulis = i['buku_pengarang']
        penerbit = i['buku_penerbit']
        tahun = i['buku_terbit_tahun']
        isbn = i['buku_isbn']
        lokasi = i['buku_terbit_lokasi']
        bahasa = i['buku_bahasa']
        ddc = i['ddc_kode']

        print('Judul :' + judul)
        print('Penulis :' + penulis)
        print('Penerbit :' + penerbit)
        print('Tahun :' + tahun)
        print('Lokasi :' + lokasi)
        print('ISBN :' + isbn)
        print('Bahasa :' + bahasa)
        print('DDC : ' + ddc)
        print()

        insert_id = general.save_db(
            judul, penulis, penerbit, tahun, lokasi, isbn, bahasa, "3", ddc)

    soup = BeautifulSoup(json.loads(source)['halaman'], 'lxml')
    paging = soup.select('ul.pagination > li > a')
    for i in paging:
        try:
            if int(i.text) == page + 1:
                scrap(s, name, int(i.text), count, i['href'])
        except Exception as e:
            pass


nama = sys.argv[1].replace('+', ' ')
s = requests.session()
scrap(s, nama)
# print()
# scrap(s, 'komputer', 2, 12)
