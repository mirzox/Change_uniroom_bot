CREATE TABLE user (
  user_id integer not null primary key,
  firstname varchar(255) not null,
  username varchar(255) not null,
  phone varchar(255) not null,
  is_admin integer default 0
);

CREATE TABLE request (
  id int not null primary key,
  potok varchar(255) not null,
  weekday varchar(255) not null,
  pairnum integer not null,
  campus varchar(255) not null,
  room varchar(255) not null,
  reason varchar(255) not null,
  status varchar(255) not null default '',
  user_id int FOREIGN KEY
);