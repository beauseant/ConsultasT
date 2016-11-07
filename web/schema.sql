drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
insert into entries ('title', 'text') values ('google','http://www.tsc.uc3m.es');
insert into entries ('title', 'text') values ('elpais','http://www.elpais.com');

drop table if exists users;
create table users (
	id integer primary key autoincrement,
	name text not null UNIQUE,
	passwd text not null
);


drop table if exists labeler;
create table labeler (
	id_user integer,
	id_entrie integer,
	date  default CURRENT_TIMESTAMP,
	id_label integer,
	primary key (id_user, id_entrie, id_label, date)
);

drop table if exists labelresult;
create table labelresult (
	id integer primary key autoincrement,
	description text not null
);

insert into labelresult ('description') values ('b2c_on');
insert into labelresult ('description') values ('b2c_ready');
insert into labelresult ('description') values ('other');
insert into labelresult ('description') values ('error');



