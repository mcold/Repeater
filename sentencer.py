# coding: utf-8
import os
import sys
from db import get_items, get_sentences, Sentence

clear = lambda: os.system('cls')
cross_line = lambda: print('\n' + '-'*25 + '\n')
num_words = 3

def get_equal_parts_plus_word(phrase: str, attempt: str) -> str:
    res = ''
    result = ''
    for char in phrase.lower():
        for char_at in attempt[len(res):].lower():
            if char == char_at:
                res = res + char
                break
            else:
                res = phrase[:len(res)]
                addition = ' '.join(phrase[len(res):].split()[0:num_words])
                if phrase[len(result)+1] == ' ':
                    res = res + ' ' + addition + ' '
                else:
                    res = res + addition + ' '
                return res
    return res

def phrase_loop(num: int, sent: Sentence):
    res = ''
    while True:
        clear()
        print('\n' + str(num) + ' ' + sent.ru)
        print('\n')
        if res == '':
            x = input()
        else:
            x = res + ' ' + input(res + ' ')
        if x.lower() != sent.eng.lower(): 
            res = get_equal_parts_plus_word(phrase=sent.eng, attempt=x)
        else:
            break

def sentence_loop(id_item: int):
    l_sents = get_sentences(id_item=id_item)
    n = 0
    for sent in l_sents:
        n = n + 1
        phrase_loop(num=n, sent=sent)

def choose_item(lang: str):
    l_items = get_items(lang)
    d_num = dict()

    for i in range(len(l_items)):
        item = l_items[i]
        d_num[i+1] = item.id
        
    while True:
        clear()
        for i in range(len(l_items)):
            print(str(i+1) + ' ' + l_items[i].name)
        cross_line()
        x = input('Enter number of item (or type exit): ')
        if x.lower() in ('exit', 'quit'):
            sys.exit()
        else:
            try:
                return d_num[int(x)]
            except KeyError:
                continue
            except ValueError:
                continue

def item_loop(lang: str):
    while True:
        sentence_loop(id_item=choose_item(lang))
        clear()

if __name__ == "__main__":
    item_loop(lang='eng')
    # item_loop(lang='eng')
    # print(get_equal_parts(phrase='sOMe ideal other maybe', attempt='Some iDeal ather maybe'))
    # if len(sys.argv) > 1:
    #     id_tech = get_tech(sys.argv[1])
    #     if id_tech is not None:
    #         topic_loop(id_tech = id_tech)
    #     else:
    #         topic_loop(choose_tech())  
    # else:
    #   topic_loop(choose_tech())