import random
import hashlib
import MySQLdb
def get_salt():
    random_source = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    salt = ''
    for i in range(16):
        salt += random.choice(random_source)
    return salt
def get_hashed_password(plain_pw, salt):
    hashed_pw = hashlib.pbkdf2_hmac('sha256', plain_pw.encode(), salt.encode(), 19720).hex()
    return hashed_pw
def get_connection():
    connection = MySQLdb.connect(user='root', password='mcmK1201', host='localhost', database='spring')
    return connection
def insert_user(name, pw, email):
    salt = get_salt()
    hashed_pw = get_hashed_password(pw, salt)
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO users (id, name, password, salt, email) VALUES (DEFAULT, %s, %s, %s, %s)'
    cursor.execute(sql, (name, hashed_pw, salt, email))
    connection.commit()
    cursor.close()
    connection.close()
def select_users():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows
def get_account_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM users WHERE email = %s'
    cursor.execute(sql, (email,))
    account = cursor.fetchone()
    cursor.close()
    connection.close()
    return account
def login(email, input_pw):
    account = get_account_by_email(email)
    if account is None:
        return None
    hashed_db_pw = account[2]
    salt = account[3]
    hashed_input_pw = get_hashed_password(input_pw, salt)
    if hashed_db_pw == hashed_input_pw:
        return account
    else:
        return None
def select_products_by_keyword(keyword):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM products WHERE name like %s'
    keyword = '%' + keyword + '%'
    cursor.execute(sql, (keyword,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows