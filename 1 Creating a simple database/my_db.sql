CREATE DATABASE IF NOT EXISTS myshop;
USE myshop;

CREATE TABLE IF NOT EXISTS clients(
id INT auto_increment PRIMARY KEY,
name CHAR(50),
age INT,
address CHAR(100)
);

CREATE TABLE IF NOT EXISTS products(
id INT AUTO_INCREMENT PRIMARY KEY,
product_name CHAR(100),
price FLOAT
);

INSERT INTO clients(name, age, address) VALUES 
("Petter Smith", 30, "Address 1"),
("Jhon Scott", 20, "Address 2"),
("Jennifer Brandon", 26, "Address 3"),
("James Benjamin", 50, "Address 4");

SELECT * FROM clients;

INSERT INTO products(product_name, price) VALUES
("Iphone X", 2000),
("TV", 900),
("Mouse", 50),
("PC", 3500),
("Shoes", 120);

SELECT * FROM products;
