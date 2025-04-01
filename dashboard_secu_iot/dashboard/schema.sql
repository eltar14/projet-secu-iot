DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS video;

CREATE TABLE credentials (
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    password_salt VARCHAR(200) NOT NULL
);

CREATE TABLE video (
    id SERIAL PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL,
    description TEXT,
    intrusion BOOLEAN DEFAULT NULL
);
