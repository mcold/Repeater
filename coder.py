# coding: utf-8
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from db import get_techs, get_tech, get_topics, get_topic_childs, get_topic_leafs, get_topic_roots, get_codes
from db import Tech, Topic

clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

def code_loop(topic: Topic, order = None):
    l_codes = get_codes(topic=topic)
    console = Console()

    clear()
    print((order + '.' if order != None else '') + ' ' + topic.name)
    empty_line()

    for i in range(len(l_codes)):
        code = l_codes[i]
        
        console.print(Markdown('\n' + (order + '.' if order != None else '') + str(i + 1) + ' ' + code.descript))
        if code.url_pict != None:
            print(str(code.url_pict))
        while input('\n') != '': continue
        console.print(Markdown(code.block))
        if code.output != None:
            while input('\n') != '': continue
            print('\n' + code.output)
        empty_line()

    while True:
        clear()
        print(topic)
        print('-'*len(topic.name) + '\n')
        do = input('Enter command or enter(to continue): \n')
        if do == 'root':
            l_leafs = get_topic_roots(topic=topic)
            for i in range(len(l_leafs)):
                print(l_leafs[i])
            empty_line()
            continue

        if do == 'child':
            l_leafs = get_topic_leafs(topic=topic)
            for i in range(len(l_leafs)):
                print(l_leafs[i])
            empty_line()
            continue
        break

    l_childs = get_topic_childs(topic=topic)
    for i in range(len(l_childs)):
        print(str(i+1) + '. ' + l_childs[i].name)
    empty_line()    

    for i in range(len(l_childs)):
        code_loop(topic = l_childs[i], order = order + '.' + str(i+1) if order != None else str(i+1))

def choose_tech() -> Tech:
    l_techs = get_techs()
    d_num = dict()
    for i in range(len(l_techs)):
        tech = l_techs[i]
        d_num[i+1] = tech.id
    
    while True:
        clear()
        for i in range(len(l_techs)):
            print(str(i+1) + ' ' + l_techs[i].name)
        cross_line()
        x = input('Enter number of tech (or type exit): ')
        if x.lower() in ('exit', 'quit') or x.lower().startswith('q') or x.lower().startswith('e'):
            sys.exit()
        else:
            try:
                return l_techs[int(x)-1]
            except KeyError:
                continue
            except ValueError:
                continue

def choose_topic(tech: Tech) -> Topic:
    l_topics = get_topics(tech=tech)
    d_num = dict()

    for i in range(len(l_topics)):
        topic = l_topics[i]
        d_num[i+1] = topic.id
        
    while True:
        clear()
        for i in range(len(l_topics)):
            print(str(i+1) + ' ' + l_topics[i].name)
        cross_line()
        x = input('Enter number of topic (or type exit): ')
        if x.lower() in ('exit', 'quit') or x.lower().startswith('q') or x.lower().startswith('e'):
            sys.exit()
        else:
            try:
                return l_topics[int(x)-1]
            except KeyError:
                continue
            except ValueError:
                continue

def topic_loop(tech: Tech):
    while True:
        topic = choose_topic(tech=tech)
        code_loop(topic=topic)
        clear()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tech = get_tech(sys.argv[1])
        if tech is not None:
            topic_loop(tech = tech)
        else:
            topic_loop(choose_tech())
    else:
      topic_loop(choose_tech())