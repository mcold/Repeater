# coding: utf-8
import sqlite3

conn = sqlite3.connect('DB.db')

cur = conn.cursor()

conn.close()