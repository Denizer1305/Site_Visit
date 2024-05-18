create table if not exists users(
id integer primary key autoincrement,
name text unique not null,
psw text not null,
time integer NOT NULL
);

create table if not exists profiles(
id integer primary key autoincrement,
user_name text unique not null,
avatar text default NULL,
name text default null,
surname text default null,
email text unique default null,
phone integer default null,
profession text default null,
about text default null,
social default null,
type_profile integer default 0
);