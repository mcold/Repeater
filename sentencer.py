# coding: utf-8
import sqlite3

conn = sqlite3.connect('DB.db')

cur = conn.cursor()

# cur.execute("SELECT * FROM users;")one_result = cur.fetchone()
cur.execute("SELECT row_number() over (partition by id_item order by seq_num asc), ru, eng FROM sentence where id_item = 1 order by seq_num asc;")
results = cur.fetchall()

for i in range(len(results)):
    print('\n' + str(results[i][0]) + ' ' + results[i][1])
    x = input()
    eng = results[i][2]
    if x != eng:
        # сравниваем фразы
        # выводим начальную совпадающую часть + 1 следующее слово
        # повторяем до тех пор пока фразы не совпадут / не будет передано действие
        pass
    
    print('\n' + results[i][2])
    x = input()

conn.close()    