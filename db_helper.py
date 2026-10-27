import sqlite3

def lookup_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return sqlite3.connect("app.db").execute(query).fetchone()
