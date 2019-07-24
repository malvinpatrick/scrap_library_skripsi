import requests
import json
from bs4 import BeautifulSoup


def scrap_detail(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    data = soup.select('tr')
    count = 1
    for i in data:
        if count == 1:
            soup2 = BeautifulSoup(str(i), 'lxml')
            temp = soup2.select('td')
            print('Pengarang : ' + temp[3])


def scrap(name):
    url = "http://katalog.wima.ac.id/result.php?kategori=title&jenis=1&vkriteria=" + name
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    list_book = soup.select('div#hsl-block')
    for i in list_book:
        soup2 = BeautifulSoup(str(i), 'lxml')
        data = soup2.select('div#infobk a')[0]
        print(data['href'])
        # title = data.text
        # print('Judul : ' + title)
        # scrap_detail(data['href'])
        # print('-----------------------------------')


scrap('komputer')
