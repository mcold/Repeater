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

class Code:
    descript = ''
    block = ''
    type = ''

    def __init__(self, t: tuple):
        self.descript = t[0]
        self.block = t[1]
        self.type = t[2]

def get_techs() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, name
                        from tech
                        order by name;
                    """)
        results = cur.fetchall()

    return [Tech(results[i]) for i in range(len(results))]

def get_tech(token: str) -> int:
    """
        Get tech by token
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id
                        from tech
                        where name like '%{token}%'
                        order by name;
                    """.format(token=token))
    result = cur.fetchone()
    if result is None:
        return None
    else:        
        return int(result[0])

def get_topics(id_tech: int) -> list:
    with sqlite3.connect(db) as conn:
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

    return [Topic(results[i]) for i in range(len(results))]

def get_codes(id_topic: int) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT descript, 
                              block, 
                              type
                FROM code 
                where id_topic = {id_topic}
                order by seq_num asc;""".format(id_topic=id_topic))
        results = cur.fetchall()

    return [Code(results[i]) for i in range(len(results))]

if __name__ == "__main__":
    print(get_tech('out'))