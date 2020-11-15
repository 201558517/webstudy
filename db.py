import sqlite3
from flask import g

DATABASE = './sqlite3.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    g.db = connect_db()