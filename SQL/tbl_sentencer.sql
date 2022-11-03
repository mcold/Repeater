create table if not exists item(id 		integer primary key autoincrement,
								lang 	text,
								name 	text,
								url 	text);
									
create table if not exists sentence(id 		integer primary key autoincrement,
									id_item integer,
									seq_num integer,
									eng 	text,
									ru 	text);