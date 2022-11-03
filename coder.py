# coding: utf-8
import sqlite3
from rich.console import Console
from rich.syntax import Syntax
from db import get_techs, get_topics


def print_topic_items():
    conn = sqlite3.connect('DB.db')

    cur = conn.cursor()
    cur.execute("""SELECT row_number() over (partition by id_topic order by seq_num asc), descript, block, type 
                FROM code where id_topic = 4
                order by seq_num asc;""")
    results = cur.fetchall()

    console = Console()

    for i in range(len(results)):
        print('\n' + str(results[i][0]) + ' ' + results[i][1])
        print('\n')
        x = input()
        synt = Syntax(results[i][2], results[i][3])
        console.print(synt)
        x = input()

    conn.close()

def choose_tech():
    l_techs = get_techs()
    d_num = dict()
    
    print('\n')
    for i in range(len(l_techs)):
        tech = l_techs[i]
        d_num[i+1] = tech.id
        print(str(i+1) + ' ' + tech.name)
    print('\n------------------------\n')
    return d_num[int(input('Enter number of tech: '))]

def choose_topic(id_tech: int):
    l_topics = get_topics(id_tech=id_tech)
    d_num = dict()
    print('\n')
    for i in range(len(l_topics)):
        topic = l_topics[i]
        d_num[i+1] = topic.id
        print(str(i+1) + ' ' + topic.name)
    print('\n------------------------\n')
    return d_num[int(input('Enter number of topic: '))]


if __name__ == "__main__":
    id_topic = choose_topic(1)
    print(id_topic)