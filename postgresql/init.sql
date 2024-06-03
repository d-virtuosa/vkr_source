-- Создание таблицы posts
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заполнение таблицы данными
INSERT INTO posts (title, category, content, created_at) VALUES ('Tech Post', 'tech', 'Some tech content', '2024-04-11');
INSERT INTO posts (title, category, content, created_at) VALUES ('Science Post', 'science', 'Some science content', '2024-04-10');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'v3ryh4rdt0brut3p@ssw0rd!');