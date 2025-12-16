
-- THIS QUERY IS ONLY FOR MICROSOFT SQL SERVER MANAGEMENT, THIS QUERY MIGHT NOT BE COMPATIBLE WITH OTHER SERVERS

create database eshop;

create table order_status(
	id int primary key identity(1,1),
	status_name nvarchar(32) not null unique
);

insert into order_status(status_name)
values ('CREATED'), ('AWAITING_PAYMENT'), ('PAID'), ('PACKING'), ('SHIPPED'), ('CANCELLED');

create table payment_status(
	id int primary key identity(1,1),
	status_name nvarchar(32) not null unique
);

insert into payment_status(status_name)
values ('INITIATED'), ('CONFIRMED'), ('FAILED'), ('REFUNDED');

create table warehouse(
	id int primary key identity(1,1) not null,
	warehouse_name nvarchar(128) not null,
	location_code varchar(128) not null,
	is_active bit not null -- can warehouse work on orders
);

create table orders(
	id int primary key identity(1,1),
	id_user int not null,
	status_id int foreign key references order_status(id) not null,
	total_amount numeric(12,2) not null check(total_amount >= 0),
	currency char(3) not null, -- iso-4217
	payment_status int foreign key references payment_status(id) not null,
	warehouse_id int foreign key references warehouse(id) not null,
	shipping_address nvarchar(128) check(isjson(shipping_address) = 1),
	billing_address nvarchar(128) check(isjson(billing_address) = 1),
	created_at timestamp not null default current_timestamp,
	updated_at timestamp not null default current_timestamp
);

create table order_items(
	id int primary key identity(1,1),
	order_id int foreign key references orders(id)
);