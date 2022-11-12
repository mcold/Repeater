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
    id_parent = 0

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_tech = t[1]
        self.name = t[2]
        self.url = t[3]
        self.id_parent = t[4]

    def __str__(self) -> str:
        return str(self.name) + '\n' + (self.url if self.url != None else '')

class Leaf:
    id = 0
    id_tech = 0
    name = ''
    url = ''
    id_parent = 0
    level = 0

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_tech = t[1]
        self.name = t[2]
        self.url = t[3]
        self.id_parent = t[4]
        self.level = t[5]

    def __str__(self) -> str:
        return ' '* 3 * self.level + str(self.name) + '\n'# (self.url if self.url != None else '')

class Code:
    descript = ''
    block = ''
    output = ''
    url_pict = ''

    def __init__(self, t: tuple):
        self.descript = t[0]
        self.block = t[1]
        self.output = t[2]
        self.url_pict = t[3]

class Item:
    id = 0
    lang = ''
    name = ''
    url = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.lang = t[1]
        self.name = t[2]
        self.url = t[3]

class Sentence:
    id = 0
    id_item = 0
    id_word = 0
    seq_num = 0
    original = ''
    ru = ''
    

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_item = t[1]
        self.id_word = t[2]
        self.seq_num = t[3]
        self.original = t[4]
        self.ru = t[5]

class Word:
    id = 0
    lang = ''
    name = ''
    ru = ''
    genus = ''
    plur_end = ''
    url = ''

    def __init__(self):
        self.id = 0
        self.lang = ''
        self.name = ''
        self.ru = ''
        self.genus = ''
        self.plur_end = ''
        self.url = ''


    def __init__(self, t: tuple):
        if len(t) == 0:
            self.id = 0
            self.lang = ''
            self.name = ''
            self.ru = ''
            self.genus = ''
            self.plur_end = ''
            self.url = ''
        else:
            self.id = t[0]
            self.lang = t[1]
            self.name = t[2]
            self.ru = t[3]
            self.genus = t[4]
            self.plur_end = t[5]
            self.url = t[6]

    def __str__(self) -> str:
        return str(self.name) + '\n' + self.genus + (', ' + self.plur_end if self.plur_end != None else '') + '\n' + (self.url if self.url != None else '')


def get_techs() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, name
                        from tech
                        order by name;
                    """)

    return [Tech(result) for result in cur.fetchall()]

def get_tech(token: str) -> int:
    """
        Get tech by token
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, name
                        from tech
                        where name like '%{token}%'
                        order by name;
                    """.format(token=token))
    result = cur.fetchone()
    if result is None:
        return None
    else:        
        return Tech(result)

def get_topics(tech: Tech) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, 
                            id_tech, 
                            name,
                            url,
                            id_parent
                        from topic
                        where id_tech = {id_tech}
                          and id_parent is null
                        order by name;
                    """.format(id_tech = tech.id))

    return [Topic(result) for result in cur.fetchall()]

def get_topic_leafs(topic: Topic) -> list:
    """
        Leaf = Topic + level
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        with recursive t(id, id_tech, name, url, id_parent, level) as
                        (
                                select id, id_tech, name, url, id_parent, 1
                                  from topic
                                 where id = {id_topic_root}
                                union all
                                select topic.id, topic.id_tech, topic.name, topic.url, topic.id_parent, t.level + 1
                                  from topic, t
                                 where topic.id_parent = t.id
                            )
                            select * 
                              from t
                             order by level asc;
                    """.format(id_topic_root = topic.id))

    return [Leaf(result) for result in cur.fetchall()]

def get_topic_roots(topic: Topic) -> list:
    """
        Leaf = Topic + level
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        with recursive t(id, id_tech, name, url, id_parent, level) as
                        (
                            select id, id_tech, name, url, id_parent, 1
                                from topic
                                where id = {id_topic_leaf}
                            union all
                            select topic.id, topic.id_tech, topic.name, topic.url, topic.id_parent, t.level + 1
                            from topic, t
                            where topic.id = t.id_parent
                            ), max_len as (select max(level) max_level from t)
                            select t.id, t.id_tech, t.name, t.url, t.id_parent, ml.max_level - t.level
                              from t, max_len ml
                             order by level desc;
                    """.format(id_topic_leaf = topic.id))
    return [Leaf(result) for result in cur.fetchall()]

def get_topic_childs(topic: Topic) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, 
                            id_tech, 
                            name,
                            url,
                            id_parent
                        from topic
                        where id_parent = {id_topic}
                        order by name;
                    """.format(id_topic = topic.id))

    return [Topic(result) for result in cur.fetchall()]

def get_codes(topic: Topic) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT descript, 
                              block,
                              output,
                              url_pict
                FROM code 
                where id_topic = {id_topic}
                order by seq_num asc;""".format(id_topic=topic.id))
    
    return [Code(result) for result in cur.fetchall()]

def get_sentences(id_item: int, id_word: int, lang: str) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        if lang is not None:
                    cur.execute("""SELECT s.id,
                                          s.id_item,
                                          s.id_word,
                                          s.seq_num,
                                          s.original,
                                          s.ru
                                    FROM sentence s,
                                             word w
                                   where id_word = w.id
                                     and w.lang = '{lang}'
                                order by random();""".format(lang=lang))
        else:                                
            if id_item is not None:
                cur.execute("""SELECT id,
                                    id_item,
                                    id_word,
                                    seq_num,
                                    original,
                                    ru
                                FROM sentence 
                                where id_item = {id_item}
                                order by random();""".format(id_item=id_item))
            else:
                if id_word is not None:
                    cur.execute("""SELECT id,
                                        id_item,
                                        id_word,
                                        seq_num,
                                        original,
                                        ru
                                    FROM sentence
                                where id_word = {id_word}
                                order by random();""".format(id_word=id_word))

    return [Sentence(result) for result in cur.fetchall()]

def get_items(lang: str) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                            lang,
                            name,
                            url
                        from item
                        where lang = '{lang}'
                        order by id desc;
                    """.format(lang = lang))

    return [Item(result) for result in cur.fetchall()]

def get_langs() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select distinct lang
                        from word
                        order by lang desc;
                    """)

    return [x[0] for x in cur.fetchall()]

def get_words(lang: str) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                            lang,
                            name,
                            ru,
                            genus,
                            plur_end,
                            url
                        from word
                        where lang = '{lang}'
                        order by name desc;
                    """.format(lang = lang))

    return [Word(result) for result in cur.fetchall()]

if __name__ == "__main__":
    print(get_tech('out'))