CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    weather TEXT NOT NULL,
    temp FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    last_call TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS user_city (
    user_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, city_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);
