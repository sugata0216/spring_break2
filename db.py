import random
import hashlib
import MySQLdb
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    sql = 'INSERT INTO users (id, name, password, salt, email, authority, point) VALUES (DEFAULT, %s, %s, %s, %s, %s, DEFAULT)'
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
def delete_products(id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'DELETE FROM products WHERE id = %s'
    cursor.execute(sql, (id,))
    connection.commit()
    cursor.close()
    connection.close()
def select_products():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM products'
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows
def delete_order_details(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'DELETE FROM order_details WHERE product_id = %s'
    cursor.execute(sql, (product_id,))
    connection.commit()
    cursor.close()
    connection.close()
def update_products(id, name, price, product_image):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE products SET name = %s, price = %s, product_image = %s WHERE id = %s'
    cursor.execute(sql, (name, price, product_image, id))
    connection.commit()
    cursor.close()
    connection.close()
def select_order_details(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM products JOIN order_details ON products.id = order_details.product_id JOIN orders ON order_details.order_id = orders.id JOIN users ON orders.user_id = users.id WHERE orders.user_id = %s'
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows
def update_point(point, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE users SET point = %s WHERE id = %s'
    cursor.execute(sql, (point, user_id))
    connection.commit()
    cursor.close()
    connection.close()
def select_recommendation():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT products.id, products.name, products.price, products.product_image, SUM(order_details.quantity) AS total_quantity FROM order_details JOIN products ON order_details.product_id = products.id GROUP BY products.id, products.name, products.price, products.product_image ORDER BY total_quantity DESC LIMIT 1'
    cursor.execute(sql)
    recommendation = cursor.fetchone()
    cursor.close()
    connection.close()
    return recommendation
def send_mail(to, subject, body):
        ID = 'k.sugata.sys24@morijyobi.ac.jp'
        PASSWORD = os.environ['MAIL_PASS']
        HOST = 'smtp.gmail.com'
        PORT = 587
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'html'))
        msg['Subject'] = subject
        msg['From'] = ID
        msg['To'] = to
        server = SMTP(HOST, PORT)
        server.starttls()
        server.login(ID, PASSWORD)
        server.send_message(msg)
        server.quit()
def update_users(user_id, name):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE users SET name = %s WHERE id = %s'
    cursor.execute(sql, (name, user_id))
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
def update_pw(email, pw):
    salt = get_salt()
    hashed_pw = get_hashed_password(pw, salt)
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE users SET password = %s, salt = %s WHERE email = %s'
    cursor.execute(sql, (hashed_pw, salt, email))
    connection.commit()
    cursor.close()
    connection.close()