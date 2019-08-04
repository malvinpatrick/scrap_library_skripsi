import requests
import json
from bs4 import BeautifulSoup

url = 'http://perpustakaan.stts.edu/index.php/FrontEnd/cariAjax'

print("URL : " + url)
# if page > 1:
#     param = {
#         'page': page
#     }
#     print("param :"+str(param))
#     books = s.get(url=url, params=param)
# else:
data = {
    'cb': 'judul',
    'submit': 'true',
    'dataCari': 'komputer',
    'jenis': 'Buku',
    'filterRb': 'cari',
}
print('data = ' + str(data))
books = requests.post(url, data=data)

source = books.text
result = json.loads(source)['hasil']
for i in result:
    print("Buku ID : " + i['buku_id'])
    print(i['buku_judul'])
