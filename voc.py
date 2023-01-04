# coding: utf-8
import typer
from os import system
from re import findall
from rich.console import Console
from rich.markdown import Markdown
from db import get_sentences, get_words, upd_sentence_view

""""
Vocabulary training module
"""

app = typer.Typer()  

clear = lambda: system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

@app.command()
def sents(lang: str = 'eng',
          type: str = None,
          word: str = None,
          order: str = 'random'):
    """
    Sentences loop
    """
    d_arg = {'lang': lang, 'type': type, 'word': word, 'order': order}
    l_sents = get_sentences(d = d_arg)
    console = Console()
    clear()
    
    for i in range(len(l_sents)):
        sent = l_sents[i]
        clear()

        console.print(Markdown('\n' + ' ' + sent.ru))
        if input('\n') == '+':
            upd_sentence_view(sentence = l_sents[i], val = 'now')
            continue
        
        console.print(Markdown(repl_reg_items(sent.original)))
        if input('\n') == '+':
            upd_sentence_view(sentence = l_sents[i], val = 'now')
            continue
        
        console.print(Markdown(sent.original))
        view_mark = input('\n')
        if view_mark == '+':
            upd_sentence_view(sentence = l_sents[i], val = 'now')
            continue
        if view_mark == '-':
            upd_sentence_view(sentence = l_sents[i], val = 'null')
            continue

@app.command()
def words(lang: str = 'eng',
          type: str = None,
          way: str = 'original',
          order: str = 'random',
          word: str = None,
          book: str = None):
    """
    Words loop
    """
    d_arg = {'lang': lang, 'type': type, 'name': word, 'book': book, 'order': order}
    l_words = get_words(d_arg)
    console = Console()
    clear()
    if way == 'ru':
        
        for i in range(len(l_words)):
            wrd = l_words[i]
            clear()

            console.print(Markdown('\n' + ' ' + wrd.ru))
            while input('\n') != '': continue
            if type == 'verb+': console.print('\n' + wrd.name.split(' ')[0])
            while input('\n') != '': continue
            console.print(Markdown('\n' + ' ' + wrd.name))
            empty_line()
    else:
        for i in range(len(l_words)):
            wrd = l_words[i]
            clear()

            console.print(Markdown('\n' + ' ' + wrd.name))
            while input('\n') != '': continue
            console.print(Markdown('\n' + ' ' + wrd.ru))
            empty_line()

@app.command()
def words_by_book(lang: str = 'eng', 
                  type: str = None, 
                  way: str = 'original', 
                  order: str = 'random', 
                  word: str = None, 
                  book: str = None):
    """
    Words loop by book
    """
    d_arg = {'lang': lang, 'type': type, 'name': word, 'book': book, 'order': order}
    l_words = get_words(d_arg)
    console = Console()
    clear()
    print(way)
    empty_line()
    if way == 'ru':
        
        for i in range(len(l_words)):
            wrd = l_words[i]
            clear()

            console.print(Markdown('\n' + ' ' + wrd.ru))
            while input('\n') != '': continue
            if type == 'verb+': console.print('\n' + wrd.name.split(' ')[0])
            while input('\n') != '': continue
            console.print(Markdown('\n' + ' ' + wrd.name))
            empty_line()
    else:
        for i in range(len(l_words)):
            wrd = l_words[i]
            clear()

            console.print(Markdown('\n' + ' ' + wrd.name))
            while input('\n') != '': continue
            console.print(Markdown('\n' + ' ' + wrd.ru))
            empty_line()            

def repl_reg_items(x: str) -> str:
    l_regs = findall(r'\[\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\]\(w*\)', x)
    for i in range(len(l_regs)): x = x.replace(l_regs[i], '[...]()')
    return x

if __name__ == "__main__":  
    app()