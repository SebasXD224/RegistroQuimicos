import sqlite3
import os

DATABASE_PATH = os.path.join("static", "databases", "dataChemical.db")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
