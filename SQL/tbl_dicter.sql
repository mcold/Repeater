create table if not exists book(id 			integer primary key autoincrement,
								author   	text,
								title 		text,
								lang 		text);

create table if not exists word(id 			integer primary key autoincrement,
								lang 		text,
								name 		text,
								ru			text,
								word		text,
								genus		text,
								plur_end 	text,
								id_book		integer,
								url 		text,
								view_date	date,
								foreign key (id_book) references book(id));