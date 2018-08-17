drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null unique,
    password text not null,
    email text not null unique,
    tag text not null unique,
    dynalist_api text not null,
    push_id text,
    push_email integer DEFAULT 1,
    push_web integer DEFAULT 1
);