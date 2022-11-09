# coding: utf-8
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from db import get_langs, get_words, get_sentences
from db import Word

clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

def sentence_loop(word: Word):
    l_sents = get_sentences(id_item = None, id_word = word.id)
    console = Console()

    clear()
    print(word)
    empty_line()

    for i in range(len(l_sents)):
        sent = l_sents[i]
        
        console.print(Markdown('\n' + str(i + 1) + ' ' + sent.ru))
        empty_line()
        console.print(Markdown(sent.original))
        empty_line()

def choose_lang() -> str:
    l_langs = get_langs()
    
    while True:
        clear()
        for i in range(len(l_langs)):
            print(str(i+1) + ' ' + l_langs[i])
        cross_line()
        x = input('Enter number of tech (or type exit): ')
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

def word_loop(lang: str):
    while True:
        word = choose_word(lang=lang)
        sentence_loop(word=word)
        clear()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        word_loop(lang = sys.argv[1])
    else:
        word_loop(choose_lang())
