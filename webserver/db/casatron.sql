drop table if exists config;
create table config (
	name text primary key,
	value text
);
insert into config values('lights.off.timestamp',datetime('now'));
insert into config values('webcam.resolution','640x480');
drop table if exists access;
create table access (
	datetime text,
	ip text,
	hostname text,
	request text,
	useragent text
);
