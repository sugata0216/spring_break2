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
def insert_user(name, pw, email, authority):
    salt = get_salt()
    hashed_pw = get_hashed_password(pw, salt)
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO users (id, name, password, salt, email, authority) VALUES (DEFAULT, %s, %s, %s, %s, %s)'
    cursor.execute(sql, (name, hashed_pw, salt, email, authority))
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
def login(email, input_pw, authority):
    account = get_account_by_email(email)
    if account is None:
        return None
    hashed_db_pw = account[2]
    salt = account[3]
    hashed_input_pw = get_hashed_password(input_pw, salt)
    if hashed_db_pw == hashed_input_pw:
        if account[5] == authority:
            return account
        else:
            return None
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
def insert_orders(user_id, total_amount):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO orders (id, user_id, total_amount, order_date) VALUES (default, %s, %s, now())'
    cursor.execute(sql, (user_id, total_amount))
    connection.commit()
    cursor.close()
    connection.close()
def insert_order_details(order_id, product_id, quantity, sub_total):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO order_details (id, order_id, product_id, quantity, sub_total) VALUES (default, %s, %s, %s, %s)'
    cursor.execute(sql, (order_id, product_id, quantity, sub_total))
    connection.commit()
    cursor.close()
    connection.close()
def select_orders():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM orders ORDER BY order_date DESC LIMIT 1'
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row
def insert_products(name, price, product_image):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO products (id, name, price, product_image) VALUES (default, %s, %s, %s)'
    cursor.execute(sql, (name, price, product_image))
    connection.commit()
    cursor.close()
    connection.close()