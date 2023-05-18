CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
	username TEXT NOT NULL UNIQUE,
	hash TEXT NOT NULL,
	account_balance TEXT DEFAULT "10000" NOT NULL
);

CREATE TABLE portfolios (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
	date_created TEXT NOT NULL,
	date_updated TEXT NOT NULL,
	user_id INTEGER NOT NULL,
	ticker TEXT NOT NULL,
	position TEXT DEFAULT "B" NOT NULL,
	size TEXT NOT NULL,
	entry_price TEXT NOT NULL,
	FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE txns (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
	date_created TEXT NOT NULL,
	date_updated TEXT NOT NULL,
	txn_type TEXT NOT NULL,
	portfolio_id INTEGER NOT NULL,
	position TEXT NOT NULL,
	size TEXT NOT NULL,
	traded_price TEXT NOT NULL,
	cash_amount TEXT NOT NULL,
	pre_balance TEXT NOT NULL,
	post_balance TEXT NOT NULL,
	FOREIGN KEY(portfolio_id) REFERENCES portfolio(id)
);