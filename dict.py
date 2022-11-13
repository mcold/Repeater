# coding: utf-8
import sys
from os import system
from re import findall
from random import shuffle
from rich.console import Console
from rich.markdown import Markdown
from db import get_langs, get_words, get_sentences, upd_sentence_view
from db import Word

clear = lambda: system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

def sentence_loop(word: Word, is_order: bool,  lang = None):
    l_sents = get_sentences(id_item = None, id_word = word.id, lang = lang, is_order = is_order)
    console = Console()

    clear()
    if word.id != 0:
        print(word)
        empty_line()
    
    if is_order:
        num = 0
        for i in range(len(l_sents)):
            num = num + 1
            sent = l_sents[i]
            console.print(Markdown('\n' + str(num) + ' ' + sent.ru))
            empty_line()
            console.print(Markdown(repl_reg_items(sent.original)))
            empty_line()
            console.print(Markdown(sent.original))
            view_mark = input('\n')

            if view_mark == '+':
                upd_sentence_view(sentence = l_sents[i], val = 'now')
            if view_mark == '-':
                upd_sentence_view(sentence = l_sents[i], val = 'null')
    else:
        l_rdm = list(range(1, len(l_sents)+1))
        shuffle(l_rdm)
        num = 0
        for i in [x-1 for x in l_rdm]:
            num = num + 1
            sent = l_sents[i]
            
            console.print(Markdown('\n' + str(num) + ' ' + sent.ru))
            empty_line()
            console.print(Markdown(repl_reg_items(sent.original)))
            empty_line()
            console.print(Markdown(sent.original))
            view_mark = input('\n')
            if view_mark == '+':
                upd_sentence_view(sentence = l_sents[i], val = 'now')
            if view_mark == '-':
                upd_sentence_view(sentence = l_sents[i], val = 'null')

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
    l_regs = findall(r'\[\w+\]\(w*\)', x)
    for i in range(len(l_regs)): x = x.replace(l_regs[i], '[...]()')
    return x

def word_loop(lang: str):
    while True:
        word = choose_word(lang=lang)
        sentence_loop(word=word)
        clear()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[2] == 'rdm':
            sentence_loop(word = Word(tuple()), lang = sys.argv[1], is_order = False)
            sys.exit()
        else:
            if sys.argv[2] == 'order':
                sentence_loop(word = Word(tuple()), lang = sys.argv[1], is_order = True)
                sys.exit()
    if len(sys.argv) > 1:
        word_loop(lang = sys.argv[1])
    else:
        word_loop(choose_lang())
