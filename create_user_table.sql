DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username char(20) NOT NULL UNIQUE,
    password char(120) NOT NULL
);