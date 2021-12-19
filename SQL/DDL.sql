drop table in_cart;
drop table order_contains;
drop table bank_account;
drop table book_order;
drop table book;
drop table billing_info;
drop table publisher;
drop table user_account;


create table user_account(
	account_ID int,
	name VARCHAR(30),
	email varchar(30),
	phone_number varchar(30),
	primary key (account_ID)
	);
	
create table publisher(
	publisher_ID int,
	name varchar(50),
	email varchar(50),
	address varchar(50),
	phone_number varchar(20),
	commission_percent int,
	primary key (publisher_ID)
	);
	
create table billing_info(
	card_number VARCHAR(20),
	billing_address VARCHAR(50),
	shipping_address VARCHAR(50),
	account_ID int,
	primary key (card_number),
	foreign key (account_ID) references user_account
	);
	
create table book(
	ISBN bigint,
	title varchar(50),
	author varchar(50),
	genre varchar(50),
	pages integer,
	price numeric(5, 2),
	stock int,
	publisher_ID int,
	primary key (ISBN),
	foreign key (publisher_ID) references publisher
	);
	
create table book_order(
	order_ID int,
	order_date date,
	tracking_ID int,
	card_number VARCHAR(20),
	account_ID int,
	primary key (order_ID),
	foreign key (card_number) references billing_info,
	foreign key (account_ID) references user_account
	);
	
create table bank_account(
	bank_account_ID int,
	balance numeric(999, 2),
	publisher_ID int,
	primary key (bank_account_ID),
	foreign key (publisher_ID) references publisher
	);
	
create table order_contains(
	ISBN bigint,
	order_ID int,
	order_amount int,
	primary key (ISBN, order_ID),
	foreign key (ISBN) references book,
	foreign key (order_ID) references book_order
	);
	
create table in_cart(
	ISBN bigint,
	account_ID int,
	cart_amount int,
	primary key (ISBN, account_ID),
	foreign key (ISBN) references book,
	foreign key (account_ID) references user_account
	);
	

	
	

	