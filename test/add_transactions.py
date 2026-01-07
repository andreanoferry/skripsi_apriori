import pandas as pd
import mysql.connector
df = pd.read_excel('dataset.xlsx')

# 2. Koneksi ke database MySQL
db_connection = mysql.connector.connect(
    host="localhost",   # Host MySQL
    user="root",        # Username MySQL
    password="",# Password MySQL
    database="salon_apriori"  # Nama database
)
cursor = db_connection.cursor()

# 3. Membuat query untuk insert data
insert_query = """
INSERT INTO salon_apriori (id_user, tanggal, customer, treatment, total) VALUES ('1', %s, %s, %s, %s,)
"""

# 4. Looping melalui data di DataFrame dan memasukkannya ke MySQL
for index, row in df.iterrows():
    cursor.execute(
    "INSERT INTO `transactions` (`id_user`, `tanggal`, `customer`, `treatment`, `total`) VALUES (%s, %s, %s, %s, %s);",
    (1, row['tanggal'], row['nama_custumer'], row['treatment'], row['total'])
)

# 5. Commit perubahan dan tutup koneksi
db_connection.commit()
cursor.close()
db_connection.close()
