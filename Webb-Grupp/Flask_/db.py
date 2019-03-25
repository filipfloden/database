import pymysql

from flask import g

def get_db():
    if "db" not in g:
        g.db = pymysql.connect("localhost", "root", "", "users")

    return g.db

    