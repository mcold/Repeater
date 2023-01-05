create table if not exists deu_prasens(id           integer primary key autoincrement,
                                        id_word 	integer references word(id) on delete cascade,
                                        ich 		text,
                                        du 			text,
                                        er_sie_es 	text,
                                        wir			text,
                                        ihr 		text,
                                        Sie 		text);
																			 
create trigger ins_word_deu_trg 
after insert on word
  begin
		insert into deu_prasens(id_word) 
		  select id
		    from word w
	       where id = new.id
			 and lang = 'deu'
			 and type = 'verb'
			 and not exists (select 1 from deu_prasens p where p.id_word = w.id);
	end;

create trigger upd_word_deu_trg 
after update on word
  begin
	insert into deu_prasens(id_word) 
	  select id
        from word w
       where id = new.id
         and lang = 'deu'
         and type = 'verb'
         and not exists (select 1 from deu_prasens p where p.id_word = w.id);

		delete
          from deu_prasens
		  where id_word = (select id
                             from word w
                            where id = new.id
                              and (lang != 'deu' or type != 'verb'));
	end;