# Database Schema
# Using root account

CREATE DATABASE IF NOT EXISTS tasks_db;

CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'qw12ERty';
CREATE DATABASE IF NOT EXISTS tasks_db;
GRANT ALL PRIVILEGES ON tasks_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE tasks_db;
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    updated_at DATETIME NOT NULL

);
CREATE TABLE IF NOT EXISTS tasks (
    task_id VARCHAR(60) PRIMARY KEY,
    user_id VARCHAR(60),
    created_at DATETIME NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    priority_level VARCHAR(100) NOT NULL,
    completion_status VARCHAR(60) NOT NULL,
    days_to_complete INT NOT NULL,
    deadline DATETIME NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
