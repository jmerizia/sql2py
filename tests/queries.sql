SELECT * FROM users WHERE age > 30;

seLect id, email , age from users
where email == ?;;

create table if not exists users (
    id INTEGER not null,
    email TEXT,
    is_admin boolean
);

drop table users;

insert into users( email , nickname, age, is_admin )
values (?, ?, ?, false) returning id;

delete FROM users where email = ?;

update users
Set email = 'admin@admin.fdsa' where id = 1;