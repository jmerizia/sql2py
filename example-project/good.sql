-- Select all users
SELECT * FROM users;

-- create a new user
INSERT INTO users (email, age) VALUES (?, ?);

-- determine if user is admin
SELECT is_admin FROM users WHERE id = ?;
