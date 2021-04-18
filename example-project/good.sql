-- Select all users
SELECT * FROM users;

-- create a new user
INSERT INTO users (email, nickname, age, is_admin) VALUES (?, ?, ?, ?);

-- determine if user is admin
SELECT is_admin FROM users WHERE id = ?;

-- get a user by email
SELECT * FROM users WHERE email = ?;

