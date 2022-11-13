create table if not exists item(id 		integer primary key autoincrement,
								lang 	text,
								name 	text,
								url 	text);
									
create table if not exists sentence(id 			integer primary key autoincrement,
									id_item 	integer,
									id_word 	integer references word(id_word),
									seq_num 	integer,
									original 	text,
									ru 			text,
									view_date	date);