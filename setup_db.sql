# Database Schema
# Using root account

CREATE DATABASE IF NOT EXISTS tasks_db;

CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'qw12ERty';
GRANT ALL PRIVILEGES ON tasks_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE tasks_db;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) NOT NULL
);
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    priority_level VARCHAR(100) NOT NULL,
    completion_status VARCHAR(60) NOT NULL,
    deadline DATETIME,
    email_address VARCHAR(100) NOT NULL
    FOREIGN KEY (user_id) REFERENCES users(id)
);