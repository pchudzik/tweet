-- migrate:up
CREATE TABLE followers (
	user_id INTEGER NOT NULL,
	follower_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, follower_id),
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(follower_id) REFERENCES users (id)
)


-- migrate:down

