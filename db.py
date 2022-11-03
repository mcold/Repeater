# coding: utf-8
import sqlite3

db = 'DB.db'

class Tech:
    id = 0
    name = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.name = t[1]

    def __str__(self) -> str:
        return str(self.id) + ': ' + str(self.name)

class Topic:
    id = 0
    id_tech = 0
    name = ''
    url = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_tech = t[1]
        self.name = t[2]
        self.url = t[3]

    def __str__(self) -> str:
        return str(self.id) + ': ' + str(self.name)

def get_techs() -> list:
    conn = sqlite3.connect(db)

    cur = conn.cursor()
    cur.execute("""
                    select id, name
                      from tech
                      order by name;
                """)
    results = cur.fetchall()
    conn.close()

    return [Tech(results[i]) for i in range(len(results))]

def get_topics(id_tech: int) -> list:
    conn = sqlite3.connect(db)

    cur = conn.cursor()
    cur.execute("""
                    select id, 
                           id_tech, 
                           name,
                           url
                      from topic
                      where id_tech = {id_tech}
                      order by name;
                """.format(id_tech = id_tech))
    results = cur.fetchall()
    conn.close()

    return [Topic(results[i]) for i in range(len(results))]

if __name__ == "__main__":
    l_topics = get_topics(1)
    print(l_topics)