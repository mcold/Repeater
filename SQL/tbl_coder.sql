create table if not exists tech(id 		integer primary key autoincrement,
								name 	text);
									
create table if not exists topic(id 		integer primary key autoincrement,
								 id_tech 	integer references tech(id) on update cascade,
								 name 		text,
								 url 		text);
									 
create table if not exists code(id 			integer primary key autoincrement,
								id_topic	integer references topic(id) on update cascade,
								seq_num		integer,
								block		blob,
								descript	text,
								output		text,
								url_pict	text);
