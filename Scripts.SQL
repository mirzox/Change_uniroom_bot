create table user
(
    user_id   integer not null
        primary key,
    firstname text,
    username  text,
    phone     text,
    is_admin  integer default 0
    lang text default 'ru'
);

create table request
(
    id      integer not null
        primary key autoincrement,
    potok   text,
    weekday text,
    pairnum integer,
    campus  text,
    room    text,
    reason  text,
    status  text default 'pending',
    user_id integer
        constraint user_id
            references user
);

