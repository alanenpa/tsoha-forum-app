
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE, 
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    header TEXT,
    init_msg TEXT,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP
);