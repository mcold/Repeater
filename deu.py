# coding: utf-8
import os
import sys
import typer
from rich.console import Console
from rich.markdown import Markdown
from db import *

""""
Deutsch training module
"""

app = typer.Typer()

clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
empty_line = lambda: input('\n')

@app.command()
def verb_tense(verb: str, tense: str = None) -> None:
    """
    Verb's tenses info
    """
    verb = get_dverbs({'name': verb})[0]
    if tense is None:
        print(verb)
        return
    if tense.lower() in ('präsens', 'prasens'):
        print(verb.dprasens)
        return


@app.command()
def verbs_train(verb: str = None, tense: str = 'Präsens'):
    """
    Verbs tenses training
    """
    verbs = get_dverbs({'word': verb})

    for verb in verbs:
        clear()
        print(verb.word)
        cross_line()
        if tense.lower() in ('präsens', 'prasens'): 
            tense_var = verb.dprasens

            for var in [x for x in tense_var.__dict__ if x.find('id') < 0]:
                while True:
                    if input(('\n{var}{space}').format(var = var.replace('_', r'/'), space = ' '*(20-len(var)))).strip().lower() == tense_var.__dict__[var]:
                        break
        clear()
    
if __name__ == "__main__":  
    app()