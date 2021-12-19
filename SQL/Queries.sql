delete from in_cart;
delete from order_contains;
delete from	bank_account;
delete from book_order;
delete from book;
delete from billing_info;
delete from publisher;
delete from user_account;


-- publishers
insert into publisher VALUES
(1, 'Firefly Books', 'ffbooks@email.com', '32 Longfields Drive', '613-100-0000', 12);

insert into publisher VALUES
(2, 'Carina Press', 'cp@email.com', '154 Upney Drive', '613-200-0000', 9);

insert into publisher VALUES
(3, 'HQN', 'hqn@email.com', '54 Upminister Street', '613-300-0000', 24);




-- books

insert into book VALUES
(4531134756586, 'The Push', 'Ahsley Audrain', 'Thriller', 662, 12.99, 13, 1);

insert into book VALUES
(8479960556995, 'A Crooked Tree', 'Una Mannion', 'Horror', 516, 13.99, 15, 1);

insert into book VALUES
(5361257320460, 'Malibu Rising', 'Taylor Jenkins Reid', 'Historical', 501, 8.99, 13, 1);

insert into book VALUES
(7201586912903, 'People We Meet on Vacation', 'Emily Henry', 'Romance', 902, 12.99, 9, 2);

insert into book VALUES
(4530158656586, 'Broken', 'Jenny Lawson', 'Comedy', 654, 19.99, 4, 2);

insert into book VALUES
(2511947576575, 'Project Hail Mary', 'Andy Weir', 'Sci-Fi', 476, 12.99, 24, 2);

insert into book VALUES
(4631814314723, 'Once There Were Wolves', 'Charlotte McConachy', 'Fiction', 235, 13.99, 42, 2);

insert into book VALUES
(5407041282692, 'The Wish', 'Nicholas Sparks', 'Fiction', 710, 12.99, 14, 2);

insert into book VALUES
(3857762924374, 'The Comfort Book', 'Matt Haig', 'Nonfiction', 86, 11.99, 23, 3);

insert into book VALUES
(3264426460768, 'Cultish', 'Amanda Montell', 'Nonfiction', 540, 12.99, 21, 3);

insert into book VALUES
(4892428994827, 'Fuzz', 'Mary Roach', 'Nonfiction', 245, 12.99, 3, 3);

insert into book VALUES
(7699497389607, 'Later', 'Stephen King', 'Horror', 775, 12.99, 11, 3);

-- Users
insert into user_account VALUES
(1, 'Feng Du', 'fengdu@cmail.carleton.ca', '613-111-1111');

-- Card
insert into billing_info VALUES
(321544351443, '54 Street', '54 Street', 1);


-- Bank Accounts
insert into bank_account VALUES
(1, 32143.21, 1);

insert into bank_account VALUES
(2, 32143.21, 2);

insert into bank_account VALUES
(3, 32143.21, 3);

-- Orders
insert into book_order VALUES
(1, '2021-6-15', 431455543, 321544351443, 1);
insert into order_contains VALUES
(2511947576575, 1, 2);
insert into order_contains VALUES
(8479960556995, 1, 1);

insert into book_order VALUES
(2, '2021-12-15', 654151344, 321544351443, 1);
insert into order_contains VALUES
(5407041282692, 2, 1);

insert into book_order VALUES
(3, '2020-6-15', 431453443, 321544351443, 1);
insert into order_contains VALUES
(2511947576575, 3, 2);
insert into order_contains VALUES
(8479960556995, 3, 1);

insert into book_order VALUES
(4, '2021-6-17', 434714443, 321544351443, 1);
insert into order_contains VALUES
(7699497389607, 4, 2);
insert into order_contains VALUES
(5361257320460, 4, 1);
insert into order_contains VALUES
(4892428994827, 4, 3);