import mysql.connector
import urllib.request

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dummy_buku"
)


def save_db(title, penulis, penerbit, tahun_terbit, lokasi_terbit, isbn, bahasa, id_perpustakaan, ddc):
    # check category
    category = ''
    if ddc != '' and ddc != None:
        ddc_category = ddc[0:3]
        category = str(int(ddc_category) / 100)
    else:
        category = None

    # INSERT DB
    mycursor = mydb.cursor()

    sql = "INSERT INTO book (judul, penulis, penerbit, tahun_terbit, lokasi_terbit, isbn, bahasa, kategori, perpustakaan, ddc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (title.upper(), penulis.upper(), penerbit.upper(),
           tahun_terbit, lokasi_terbit.upper(), isbn, bahasa.upper(), category, id_perpustakaan, ddc)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.lastrowid


def save_thumbnail(url, id):
    urllib.request.urlretrieve(
        url, "thumbnail/" + str(id) + ".jpg")
