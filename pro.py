# coding: utf-8
import os
import sys
import typer
from rich.console import Console
from rich.markdown import Markdown
from db import *

""""
Coder training module
"""

app = typer.Typer()

clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

@app.command()
def tech_list():
    """
    Technologies list
    """
    for tech in get_techs(): print(tech.name)

@app.command()
def topic_list(tech: str = None):
    """
    Topics list
    """
    if not tech:
        print("No value for 'tech' argument")
        sys.exit(1)
    for topic in get_topics(tech=get_tech(token = tech)): print(topic.name)

@app.command()
def topic_loop(name: str  = None, order: str = None):
    """
    Topic's snippets repeat
    """    
    topic = get_topic(token = name)
    l_codes = get_codes(topic = topic)
    console = Console()

    clear()
    print((order + '.' if order != None else '') + ' ' + topic.name + ('\n' + topic.url if topic.url != None else '') )
    empty_line()

    for i in range(len(l_codes)):
        code = l_codes[i]
        
        console.print(Markdown('\n' + code.descript))
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
        topic_loop(name = l_childs[i].name, order = order + '.' + str(i+1) if order != None else str(i+1))

    while True:
        view_mark = input('Result (+/-): ')
        if view_mark == '+':
            upd_topic_view(topic = topic, val = 'now')
            break
        if view_mark == '-':
            upd_topic_view(topic = topic, val = 'null')
            break

if __name__ == "__main__":  
    app()