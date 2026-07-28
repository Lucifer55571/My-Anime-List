BEGIN TRANSACTION;
CREATE TABLE anime (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	genre VARCHAR(100) NOT NULL, 
	studio VARCHAR(100) NOT NULL, 
	episodes INTEGER NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	score FLOAT NOT NULL, 
	release_year INTEGER NOT NULL, 
	cover_url VARCHAR(500), 
	synopsis TEXT, 
	created_at DATETIME, 
	updated_at DATETIME, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
COMMIT;
