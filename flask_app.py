"""
Flask application

The main page just re-directs to /recipes since that is
the most relevant page anyway. And who wants a 'Welcome here' page anyway?
"""
import os
import re
from copy import deepcopy
from flask import Flask, render_template, redirect, url_for
from enum import Enum
from datetime import datetime


import sqlite3

app = Flask(__name__)

class PEE_OR_POO(Enum):
    PEE = "KISS"
    POO = "BAJS"

class HIT_OR_MISS(Enum):
  HIT = "TRÄFF"
  MISS = "MISS"


def connect_to_db():
    """
    Connect to db and return the cursor
    """
    # Connect to database
    try:
        sqliteConnection = sqlite3.connect('kissochbajs.db')
        cursor = sqliteConnection.cursor()
        return cursor
    except Exception as e:
        print("Failed to connect to database")
        return NULL


"""
 Example
"INSERT INTO `records` (`time`, `type`, `result`) VALUES (%s, %s, %s)"
"""


# change this to add to database
def add_to_db(pee_or_poo = False, hit_or_miss=False):
    """Add chosen recipe to the shopping list"""
    cursor = connect_to_db()
    if cursor:
        # Write to database
        print("Writing to database")
        if not pee_or_poo:
            print("You need to specify if it was a pee or poo")
        else:
            if pee_or_poo == PEE_OR_POO.PEE:
              now = datetime.now()
              now_str = now.strftime("%d/%m/%Y %H:%M:%S")
              query = f"INSERT INTO `records` (`time`, `type`, `result`) VALUES ('{now_str}', '{pee_or_poo.value}', '{hit_or_miss.value}')"
              cursor.execute(query)
              print(f"{pee_or_poo.value} {hit_or_miss.value}")
    else:
        print("Failed to connect to database.")


def goto_mainpage():
  return redirect(url_for('mainpage'))
    
@app.route("/kiss/")
def add_kiss():
  return render_template("kiss.html")

@app.route("/kiss_hit/")
def add_kiss_hit():
  add_to_db(PEE_OR_POO.PEE, HIT_OR_MISS.HIT)
  return goto_mainpage()

@app.route("/kiss_miss/")
def add_kiss_miss():
  add_to_db(PEE_OR_POO.PEE, HIT_OR_MISS.MISS)
  return goto_mainpage()

@app.route("/bajs/")
def add_bajs():
  return render_template("bajs.html")

@app.route("/bajs_hit/")
def add_bajs_hit():
  add_to_db(PEE_OR_POO.POO, HIT_OR_MISS.HIT)
  return goto_mainpage()

@app.route("/bajs_miss/")
def add_bajs_miss():
  add_to_db(PEE_OR_POO.POO, HIT_OR_MISS.MISS)
  return goto_mainpage()

@app.route("/")
def home():
  """Home page. Redirects to recipes page"""
  return mainpage()


@app.route("/base/")
def mainpage():
    """
    Show the recipes page. A lot of data mangling happens here.
    Accessible via menu bar.
    """
    cursor = connect_to_db()
    return render_template("base.html")


import os

def main(ip="0.0.0.0"):
    """Start the application. Entry point for the flask application"""
    # Load or create database
    if not os.path.exists("kissochbajs.db"):
        print("Could not find db. Populating new one")
        cursor = connect_to_db()
        # Create records table
        sql_create_records_table = """ CREATE TABLE IF NOT EXISTS records (
                                       time text PRIMARY KEY,
                                       type text NOT NULL,
                                       result text NOT NULL
                                   ); """
        cursor.execute(sql_create_records_table)

    # Start application
    app.run(debug=False, host=ip)


if __name__ == "__main__":
    main()
