# coding: utf-8
import os
import sys
from rich.console import Console
from rich.syntax import Syntax
from db import get_techs, get_tech, get_topics, get_codes


clear = lambda: os.system('cls')

def print_codes(id_topic: int):
    l_codes = get_codes(id_topic=id_topic)
    console = Console()

    for i in range(len(l_codes)):
        code = l_codes[i]
        print('\n' + str(i + 1) + ' ' + code.descript)
        _ = input('\n')
        synt = Syntax(code.block, code.type)
        console.print(synt)
        _ = input('\n')

def choose_tech():
    l_techs = get_techs()
    d_num = dict()
    for i in range(len(l_techs)):
        tech = l_techs[i]
        d_num[i+1] = tech.id
    
    while True:
        clear()
        for i in range(len(l_techs)):
            print(str(i+1) + ' ' + l_techs[i].name)
        print('\n------------------------\n')
        x = input('Enter number of tech (or type exit): ')
        if x.lower() in ('exit', 'quit'):
            sys.exit()
        else:
            try:
                return d_num[int(x)]
            except KeyError:
                continue
            except ValueError:
                continue

def choose_topic(id_tech: int):
    l_topics = get_topics(id_tech=id_tech)
    d_num = dict()

    for i in range(len(l_topics)):
        topic = l_topics[i]
        d_num[i+1] = topic.id
        
    while True:
        clear()
        for i in range(len(l_topics)):
            print(str(i+1) + ' ' + l_topics[i].name)
        print('\n------------------------\n')
        x = input('Enter number of topic (or type exit): ')
        if x.lower() in ('exit', 'quit'):
            sys.exit()
        else:
            try:
                return d_num[int(x)]
            except KeyError:
                continue
            except ValueError:
                continue

def topic_loop(id_tech: int):
    while True:
        id_topic = choose_topic(id_tech)
        print_codes(id_topic=id_topic)
        clear()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        id_tech = get_tech(sys.argv[1])
        if id_tech is not None:
            topic_loop(id_tech = id_tech)
        else:
            topic_loop(choose_tech())  
    else:
      topic_loop(choose_tech())