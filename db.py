# coding: utf-8
import sqlite3

db = 'DB.db'
cross_len = 40
dif = 5


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
    
    def __str__(self):
        return '{id}: id_word = {id_word}: {original}'.format(id = self.id, id_word = self.id_word, original = self.original)

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
        self.type = ''


    def __init__(self, t: tuple):
        if len(t) == 0:
            self.id = 0
            self.lang = ''
            self.name = ''
            self.ru = ''
            self.genus = ''
            self.plur_end = ''
            self.url = ''
            self.type = ''
        else:
            self.id = t[0]
            self.lang = t[1]
            self.name = t[2]
            self.ru = t[3]
            self.genus = t[4]
            self.plur_end = t[5]
            self.url = t[6]
            self.type = t[7]

    def __str__(self) -> str:
        l_str = []
        if self.genus != None:
            l_str.append(self.genus)
        if self.plur_end != None:
            l_str.append(self.plur_end)
        return '{name}\n{ru}\n{other}'.format(
                                    name = self.name,
                                    ru =  '{ru}'.format(ru = self.ru) if self.ru != None else '',
                                    other = '{other}'.format(other = ",".join(l_str) + ('\n' + self.url if self.url != None else ''))
                            )
class DPrasens:
    id = 0
    id_word = 0
    ich = ''
    du = ''
    er_sie_es = ''
    wir = ''
    ihr = ''
    Sie = ''
    tense = 'Pr??sens'

    def __init__(self, t: tuple) -> None:
        if len(t) == 0:
            self.id = 0
            self.id_word = 0
            self.ich = ''
            self.du = ''
            self.er_sie_es = ''
            self.wir = ''
            self.ihr = ''
            self.Sie = ''
        else:
            self.id = t[0]
            self.id_word = t[1]
            self.ich = t[2]
            self.du = t[3]
            self.er_sie_es = t[4]
            self.wir = t[5]
            self.ihr = t[6]
            self.Sie = t[7]

    def __str__(self) -> str:
        global cross_len
        global dif
        return """\n{title}
                  \nich\t\t{ich}
                  \ndu\t\t{du}
                  \ner/sie/es\t{er_sie_es}
                  \nwir\t\t{wir}
                  \nihr\t\t{ihr}
                  \nSie\t\t{Sie}
               """.format(title='-' * dif + ' ' + self.tense + ' ' + '-'*(cross_len - dif - len(self.tense) - 2),
                          ich = self.ich,
                          du = self.du,
                          er_sie_es = self.er_sie_es,
                          wir = self.wir,
                          ihr = self.ihr,
                          Sie = self.Sie)

class DVerb:
    word = Word(tuple())
    dprasens = DPrasens(tuple())

    def __init__(self, w: Word) -> None:
        self.word = w
        self.dprasens = get_dprasent(self.word.id)
    
    def __str__(self) -> str:
        global cross_len
        return '{cross}\n{word}{dprasens}'.format(cross = '-'*cross_len,
                                                word = self.word.__str__(), 
                                                dprasens = self.dprasens.__str__())

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

def get_topic(token: str) -> Topic:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id, 
                            id_tech, 
                            name,
                            url,
                            id_parent
                        from topic
                        where name like '%{token}%';
                    """.format(token=token))
    result = cur.fetchone()
    if result is None:
        return None
    else:        
        return Topic(result)

def get_topics_order(tech: Tech) -> list:
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
                        order by view_date asc, id asc
                        nulls first;
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

def get_sentences(d: dict) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT s.id,
                              s.id_item,
                              s.id_word,
                              s.seq_num,
                              s.original,
                              s.ru
                         FROM sentence s,
                                word w
                    where 1=1 
                        and id_word = w.id
                        {lang_condition} {item_condition} {word_condition} {type_condition}
                order by {order};""".format(
                                    lang_condition="\nand w.lang = '{lang}'".format(lang=d.get('lang')) if d.get('lang') != None else '',
                                    item_condition="\nand s.id_item = {id_item}".format(id_item=d.get('id_item')) if d.get('id_item') != None else '',
                                    word_condition="\nand lower(w.name) like lower('%{word}%')".format(word=d.get('word')) if d.get('word') != None else '',
                                    type_condition="\nand w.type = '{type}'".format(type=d.get('type')) if d.get('type') != None else '',
                                    order="\ns.view_date asc, s.id asc nulls first" if d.get('order') == 'order' else 'random()')
                                    )

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

def get_words(d: dict) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select w.id,
                               w.lang,
                               w.name,
                               w.ru,
                               w.genus,
                               w.plur_end,
                               w.url,
                               w.type
                        from word w
                        left join book b on w.id_book = b.id
                        where 1=1
                          {lang_condition} {type_condition} {name_condition} {book_condition}
                        order by {order};""".format(
                                              lang_condition="\nand lower(w.lang) = lower('{lang}')".format(lang=d.get('lang')) if d.get('lang') != None else '',
                                              type_condition="\nand lower(w.type) = lower('{type}')".format(type=d.get('type')) if d.get('type') != None else '',
                                              name_condition="\nand lower(w.name) like lower('%{name}%')".format(name=d.get('word')) if d.get('word') != None else '',
                                              book_condition="\nand lower(b.title) like lower('%{title}%')".format(title=d.get('book')) if d.get('book') != None else '',
                                              order="\nrandom()" if d.get('order') == 'random' else 'w.name')
                                              )

    return [Word(result) for result in cur.fetchall()]

def get_dverbs(d: dict) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select w.id,
                               w.lang,
                               w.name,
                               w.ru,
                               w.genus,
                               w.plur_end,
                               w.url,
                               w.type
                        from word w
                        left join book b on w.id_book = b.id
                        where 1=1
                          and w.lang = 'deu'
                          and w.type = 'verb'
                          {name_condition}{book_condition}
                        order by {order};""".format(
                                              name_condition="\nand lower(w.name) like lower('%{name}%')".format(name=d.get('word')) if d.get('word') != None else '',
                                              book_condition="\nand lower(b.title) like lower('%{title}%')".format(title=d.get('book')) if d.get('book') != None else '',
                                              order="\nrandom()" if d.get('order') == 'random' else 'w.name')
                                              )

    return [DVerb(Word(result)) for result in cur.fetchall()]

def get_dprasent(id_word: int) -> DPrasens:
    with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                            select id, 
                                id_word, 
                                ich,
                                du,
                                er_sie_es,
                                wir,
                                ihr,
                                Sie
                            from deu_prasens
                            where id_word = {id_word};
                        """.format(id_word=id_word))
            
            result = cur.fetchone()
            if result is None:
                return None
            else:        
                return DPrasens(result)

def upd_topic_view(topic: Topic, val: str):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute( """update topic
                        set view_date = datetime('{val}','localtime')
                        where id = {id_topic}
                    """.format(id_topic = topic.id, val = val))

def upd_sentence_view(sentence: Sentence, val: str):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute( """update sentence
                        set view_date = datetime('{val}','localtime')
                        where id = {id_sent}
                    """.format(id_sent = sentence.id, val = val))

if __name__ == "__main__":
    print(get_tech('out'))