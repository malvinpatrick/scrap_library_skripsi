import requests
import json
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
import sys
import general


def scrap_detail(title, url, count):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    jenis = soup.select('.contentContainer table td')[0].select('span')[0].text
    if(jenis == 'Lihat Detail Buku'):
        data = soup.select('table')[4]

        details = data.select('tr')

        ddc = details[0].select('td')[3].text.split(' ')
        pengarang = details[2].select('td')[2].select('a')[0].text
        penerbit = details[3].select('td')[2].text
        penerbit = "".join(line.strip() for line in penerbit.split("\n"))
        isbn = details[5].select('td')[2].text
        isbn = "".join(line.strip() for line in isbn.split("\n"))
        if isbn == '':
            isbn = '-'

        temp = penerbit.split(':')
        print("Buku KE-" + str(count))
        print('Title : ' + title)
        print('Pengarang : ' + pengarang)
        print('Penerbit : ' + temp[1].split(',')[0][1:])
        print('Lokasi Terbit : ' + temp[0])
        print('Tahun Terbit : ' + temp[1].split(',')[1][1:])
        print('ISBN : ' + isbn)
        print('Bahasa : Indonesia')
        print("Old DDC : " + details[0].select('td')[3].text)
        new_ddc = None
        index = None
        for idx, text in enumerate(ddc):
            for i in text:
                if i.isalpha():
                    index = idx
                    print("Index : " + str(index))
                    break
            if index != None:
                break
        if index != None:
            # A 123.123
            if len(ddc) > 1 and index == 0 and not ddc[1][0].isalpha():
                new_ddc = ddc[1]
            elif index > 0:  # 123.132 A
                new_ddc = ddc[0]
        else:  # 123.123
            new_ddc = ddc[0]

        print('DDC : ' + ('-' if new_ddc == None else new_ddc))
        count = count + 1

        insert_id = general.save_db(
            title, pengarang, temp[1].split(',')[0][1:], temp[1].split(',')[1][1:], temp[0], isbn, 'Indonesia', "2", new_ddc)

        url_image = soup.select('#imgfoto')[0]['src']
        # cek thumbnail buku
        try:
            request = requests.head(url_image)
            general.save_thumbnail(url_image, str(insert_id))
            print("Thumbnail : YES")
        except Exception as e:
            print("Thumbnail : NO")

        print()
    return count


def scrap(name, page_now=1, count=1):
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

        # Detail Book
        link_detail = str(i.select('td')[0].select('a')[0]['href'])
        temp_count = scrap_detail(title, link_detail, count)
        count = temp_count

    pagination = data.select('tr')[-1].select('a')
    # current page doesn't have element <a>
    for i in pagination:

        link = 'http://digilib.ubaya.ac.id/index.php' + i['href']
        parsed = parse_qs(urlparse(link).query)['pages']
        pages = int(parsed[0])

        if page_now + 1 == pages:
            scrap(link, pages, count)


keyword = sys.argv[1]
scrap(keyword)
