import config as CFG
import mysql.connector


# koneksi ke database
def conn(user=CFG.DATABASE_NAME_USER, password=CFG.DATABASE_PASSWORD, host=CFG.DATABASE_LOCALHOST, database=CFG.DATABASE_NAME_DB):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    return conn


# Perintah Query Select ke JSON
def select(query, values, conn):
    mycursor = conn.cursor()
    mycursor.execute(query, values)
    row_headers = [x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    return json_data


# Perintah Query Insert
def insert(query, val, conn):
    mycursor = conn.cursor()
    mycursor.execute(query, val)
    conn.commit()
