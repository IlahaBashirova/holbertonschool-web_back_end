-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO 'root'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256),
    email VARCHAR(256),
    password VARCHAR(256),
    ssn VARCHAR(256),
    phone VARCHAR(256)  
);

-- insert sample data
INSERT INTO users (name, email, password, ssn, phone) VALUES
('John Doe', 'john@doe.com', 'password123', '123-45-6789', '555-1234'),
('Jane Smith', 'jane@smith.com', 'password456', '987-65-4321', '555-5678');
