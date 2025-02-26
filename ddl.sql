CREATE DATABASE spring;
CREATE TABLE products(
    id  INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL,
    product_image TEXT NOT NULL
);
CREATE TABLE users(
    id  INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    password CHAR(64) NOT NULL,
    salt CHAR(16) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    authority INTEGER NOT NULL
);
CREATE TABLE orders(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    order_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE order_details(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sub_total INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);