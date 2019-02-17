-- migrate:up
CREATE TABLE users (
	id serial NOT NULL,
	name VARCHAR(256) not null,
	password VARCHAR(62564) not null,
	PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE TABLE tweets (
	id SERIAL NOT NULL,
	content VARCHAR(256),
	user_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES users (id)
)

-- migrate:down
