create table if not exists  dialog(id 	integer primary key autoincrement,
  	  							   name text,
	  							   url 	text);
									
create table if not exists user(id    integer primary key autoincrement,
								name  text);
									
create table if not exists phrase(id 	   integer primary key autoincrement,
                                 id_dialog integer references dialog(id) on update cascade,
                                 id_user   integer references user(id) on update cascade,
                                 seq_num   integer,
                                 eng 	   text,
                                 ru		   text);