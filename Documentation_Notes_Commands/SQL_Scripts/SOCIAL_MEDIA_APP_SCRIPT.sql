--------------------------FAST API SOCIAL MEDIA APPLICATION SQL SCRIPT ----------------------------------------------

create table social_media_posts(
		id serial primary key,
		title varchar(1000) not null,
		content varchar not null,
		published bool default true,
		created_at timestamp with time zone not null default now()
);


insert into fastapi_db.public.social_media_posts (title, content, published) values ('first post', 'my first post !!!!', true),
											   ('second post', 'my second post !!!', true);
											  
insert into fastapi_db.public.posts (title, content, published) values ('first post', 'my first post !!!!', true),
											   ('second post', 'my second post !!!', true);
											  
insert into fastapi_db.public.users (id, email, password) values(1, 'john@gmail.com', 'abcd'),
																(2, 'cindy@gmail.com', 'abcde');
											   
delete from fastapi_db.public.social_media_posts ;