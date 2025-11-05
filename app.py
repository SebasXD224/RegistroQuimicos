from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

DATABASE_PATH = os.path.join("static", "databases", "dataChemical.db")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route("/")
def records():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Record ORDER BY id_record DESC")
        records = cursor.fetchall()

    return render_template("records.html", records=records)


@app.route("/addRecord")
def addRecord():
    return render_template("addRecord.html")


@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


if __name__ == "__main__":
    app.run(debug=True)
