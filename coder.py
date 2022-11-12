# coding: utf-8
import os
import sys
from random import shuffle
from rich.console import Console
from rich.markdown import Markdown
from db import get_techs, get_tech, get_topics, get_topic_childs, get_topic_leafs, get_topic_roots, get_codes, upd_topic_view, get_topics_order
from db import Tech, Topic


clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

def code_loop(topic: Topic, order = None):
    l_codes = get_codes(topic=topic)
    console = Console()

    clear()
    print((order + '.' if order != None else '') + ' ' + topic.name + ('\n' + topic.url if topic.url != None else '') )
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

    while True:
        view_mark = input('Result (+/-): ')
        if view_mark == '+':
            upd_topic_view(topic = topic, val = 'now')
            break
        if view_mark == '-':
            upd_topic_view(topic = topic, val = 'null')
            break

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

def topic_loop(tech: Tech, is_rdm: bool, is_order: bool):
    if is_rdm:
        l_topics = get_topics(tech=tech)
        l_rdm = list(range(1, len(l_topics)+1))
        shuffle(l_rdm)
        for i in range(len(l_rdm)):
            code_loop(topic=l_topics[i])
            clear()
    else:
        if is_order:
            l_topics = get_topics_order(tech=tech)
            for i in range(len(l_topics)):
                code_loop(topic=l_topics[i])
                clear()
        else:        
            while True:
                topic = choose_topic(tech=tech)
                code_loop(topic=topic)
                clear()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[2] == 'rdm':
            tech = get_tech(sys.argv[1])
            if tech is not None:
                topic_loop(tech = tech, is_rdm=True, is_order=False)
                sys.exit()
            else:
                topic_loop(choose_tech(), is_rdm=True, is_order=False)
        else:
            if sys.argv[2] == 'order':
                tech = get_tech(sys.argv[1])
                if tech is not None:
                    topic_loop(tech = tech, is_rdm=False, is_order=True)
                    sys.exit()
                else:
                    topic_loop(choose_tech(), is_rdm=False, is_order=True) 
    if len(sys.argv) > 1:
        tech = get_tech(sys.argv[1])
        if tech is not None:
            topic_loop(tech = tech, is_rdm=False, is_order=False)
        else:
            topic_loop(choose_tech(), is_rdm=False, is_order=False)
    else:
      topic_loop(choose_tech(), is_rdm=False, is_order=False)