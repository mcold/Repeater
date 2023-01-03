# coding: utf-8
import sys
from os import system
from re import findall
from rich.console import Console
from rich.markdown import Markdown
from db import get_langs, get_words
from db import Word

clear = lambda: system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')


def word_loop(d_arg: dict):
    l_words = get_words(d_arg)
    console = Console()
    clear()

    for i in range(len(l_words)):
        wrd = l_words[i]
        clear()

        console.print(Markdown('\n' + ' ' + wrd.name))
        empty_line()
        console.print(Markdown('\n' + ' ' + wrd.ru))
        empty_line()

def choose_lang() -> str:
    l_langs = get_langs()
    
    while True:
        clear()
        for i in range(len(l_langs)):
            print(str(i+1) + ' ' + l_langs[i])
        cross_line()
        x = input('Enter number of lang (or type exit): ')
        if x.lower() in ('exit', 'quit') or x.lower().startswith('q') or x.lower().startswith('e'):
            sys.exit()
        else:
            try:
                return l_langs[int(x)-1]
            except KeyError:
                continue
            except ValueError:
                continue

def choose_word(lang: str) -> Word:
    l_words = get_words(lang=lang)
    d_num = dict()

    for i in range(len(l_words)):
        topic = l_words[i]
        d_num[i+1] = topic.id
        
    while True:
        clear()
        for i in range(len(l_words)):
            print(str(i+1) + ' ' + l_words[i].name)
        cross_line()
        x = input('Enter number of word (or type exit): ')
        if x.lower() in ('exit', 'quit') or x.lower().startswith('q') or x.lower().startswith('e'):
            sys.exit()
        else:
            try:
                return l_words[int(x)-1]
            except KeyError:
                continue
            except ValueError:
                continue

def repl_reg_items(x: str) -> str:
    l_regs = findall(r'\[\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\]\(w*\)', x)
    for i in range(len(l_regs)): x = x.replace(l_regs[i], '[...]()')
    return x

if __name__ == "__main__":
    d_arg = dict([(arg.split('=')[0], arg.split('=')[1]) for arg in sys.argv[1:]])
    if d_arg.get('lang') is None: d_arg['lang'] = choose_lang()
    word_loop(d_arg)