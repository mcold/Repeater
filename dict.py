# coding: utf-8
import typer
from os import system
from re import findall
from rich.console import Console
from rich.markdown import Markdown
from db import get_sentences, get_words, upd_sentence_view

app = typer.Typer()  

clear = lambda: system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

@app.command()
def sents(lang: str = 'eng', type: str = None, word: str = None, order: str = 'random'):
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
def words(lang: str = 'eng', type: str = None, name: str = None, book: str = None):
    d_arg = {'lang': lang, 'type': type, 'name': name, 'book': book}
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

def repl_reg_items(x: str) -> str:
    l_regs = findall(r'\[\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\]\(w*\)', x)
    for i in range(len(l_regs)): x = x.replace(l_regs[i], '[...]()')
    return x

if __name__ == "__main__":  
    app()