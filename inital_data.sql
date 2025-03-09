drop table if exists user;
create table test.user(
    uid bigint auto_increment primary key,
    name varchar(100) not null
    grade tinyint not null,
    indate timestamp not null
);


drop table if exists sid;
create table test.sid(
    sid integer auto_increment primary key,
    uid bigint not null,
    date timestamp not null now(),
);

drop table if exists reserv_log;
create table test.reservation(
    sid integer auto_increment primary key,
    uid bigint not null,
    date timestamp not null,
);




truncate table blog;