--table 1: buyer
CREATE TABLE IF NOT EXISTS buyer(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	name VARCHAR(128) NOT NULL,
	phone_number INTEGER UNIQUE NOT NULL CHECK (phone_number BETWEEN 80000000 AND 99999999),
	hall VARCHAR(8) NOT NULL CHECK (hall IN  ('RH','TH','SH', 'KR','EH','PGP','KE7','PGP')),
	wallet_balance INTEGER NOT NULL CHECK (wallet_balance >= 5),
	UNIQUE (username,hall)); 

--table 2: shop
CREATE TABLE IF NOT EXISTS shop(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	shopname VARCHAR(128) UNIQUE NOT NULL,
	opening TIME(0),
	closing TIME(0),
	UNIQUE (shopname,opening,closing)
	);

--table 3: item
CREATE TABLE IF NOT EXISTS item(
	shopname VARCHAR(32) REFERENCES shop(shopname),
	item VARCHAR(32) NOT NULL,
	price MONEY NOT NULL,
	PRIMARY KEY (shopname, item),
	UNIQUE (shopname,item)
);

--table 4: orderid
CREATE TABLE IF NOT EXISTS orderid(
	group_order_id INTEGER PRIMARY KEY,
	creator VARCHAR(32),
	hall VARCHAR(8),
	shopname VARCHAR(32),
	opening TIME(0),
	closing TIME(0),
	order_date DATE,
	order_by TIME(0) -- get data from mockaroo auto-generated --
	CHECK (order_by > opening AND order_by < closing),
	delivery_status VARCHAR(32)
	CHECK (delivery_status IN ('Order Received', 'Vendor Preparing', 
							   'Food Dispatched', 'Food Delivered')),
	FOREIGN KEY(shopname, opening, closing) REFERENCES shop(shopname, opening, closing),
	FOREIGN KEY (creator, hall) REFERENCES buyer(username, hall)
	
);

--table 5: orders
CREATE TABLE IF NOT EXISTS orders(
	username VARCHAR(32) REFERENCES buyer(username),
	group_order_id INTEGER REFERENCES orderid(group_order_id),
	shopname VARCHAR(32),
	item VARCHAR(32),
	qty INTEGER NOT NULL CHECK(qty >= 1),
	FOREIGN KEY (shopname,item) REFERENCES item(shopname,item),
	PRIMARY KEY (username, group_order_id, item));
	
