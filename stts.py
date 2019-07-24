import requests
import json
from bs4 import BeautifulSoup

books = requests.post('http://perpustakaan.stts.edu/index.php/FrontEnd/cariAjax', data={
    'submit': 'true',
    'dataCari': 'komputer',
    'jenis': 'Buku',
    'filterRb': 'cari'
})

source = books.text
result = json.loads(source)['hasil']

data = []
# for i in result:
#     print(i['buku_judul'])

soup = BeautifulSoup(json.loads(source)['halaman'], 'lxml')
paging = soup.select('ul li a')

for i in paging:
    print(i['href'])


def scrap(name, page=1, offset=0):
    if offset != 0:
        url += '/' + offset

    if page != 1:
        url += '?page=' + page

    books = requests.post('http://perpustakaan.stts.edu/index.php/FrontEnd/cariAjax', data={
        'submit': 'true',
        'dataCari': 'komputer',
        'jenis': 'Buku',
        'filterRb': 'cari'
    })
    source = books.text
    result = json.loads(source)['hasil']
    for i in result:
        print(i['buku_judul'])

    soup = BeautifulSoup(json.loads(source)['halaman'], 'lxml')
    paging = soup.select('ul li a')
    get_pagination(paging)


def get_pagination(name, paging, now=1):
    for i in paging:
        if i.text != '< First' and i.text != '<' and i.text != '>' and i.text != 'Last >':
            print(i.text)
            scrap(name, i.text, )
