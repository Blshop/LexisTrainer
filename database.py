import sqlite3

def create_commection(db_file):
    conn = sqlite3.connect(db_file)



create_commection('.\Languages')