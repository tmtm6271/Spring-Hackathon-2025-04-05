
DROP DATABASE chat_app_db;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    signup_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE,
    room_name VARCHAR(255) UNIQUE NOT NULL,
    visibility INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE room_members(
    room_member_id INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    privilege VARCHAR(255) NOT NULL,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE files(
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY(message_id) REFERENCES messages(message_id) ON DELETE CASCADE,
    display_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL
)

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (room_member_id) REFERENCES room_members(room_member_id) ON DELETE CASCADE,
    file_id INT,
    original_message VARCHAR(10000) NOT NULL,
    translated_message VARCHAR(10000) DEFAULT NULL,
    first_sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO companies(company_name) VALUES ('テスト株式会社');
INSERT INTO users(user_id, company_id, user_name, email, pass) VALUES
    ('test_user_0001', 1, 'テストユーザー1', 'test1@gmail.com', 'testest1'),
    ('test_user_0002', 1, 'テストユーザー2', 'test2@gmail.com', 'testest2'),
    ('test_user_0003', 1, 'テストユーザー3', 'test3@gmail.com', 'testest3');
INSERT INTO rooms(owner_id, room_name) VALUES('test_user_0001', 'ぼっち部屋');
INSERT INTO room_members(user_id, room_id, privilege) VALUES
    ('test_user_0001', 1, 'admin'),
    ('test_user_0002', 1, 'member');