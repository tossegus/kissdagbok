"""
Flask application

The main page just re-directs to / since that is
the most relevant page anyway.

And who wants a 'Welcome here' page anyway?
"""
import os
import re
from copy import deepcopy
from flask import Flask, render_template, redirect, url_for
from enum import Enum
from datetime import datetime
from math import ceil

from contextlib import contextmanager

import sqlite3

app = Flask(__name__)

class PEE_POO_CLOCKED(Enum):
    PEE     = 128166 #"KISS"
    POO     = 128169 #"BAJS"
    CLOCKED = 128337 #"RUTIN"

class HIT_OR_MISS(Enum):
    HIT           = 11088  #"TRÄFF" This number is a star
    MISS          = 10060  #"MISS" This number is a red cross
    MIXED_SUCCESS = 127906 #"OSÄKERT" This is a roller coaster

@contextmanager
def connect_to_db(write = False):
    """
    Connect to db and return the cursor
    """
    # Connect to database
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        yield cursor
    except Exception as e:
        print("Failed to connect to database")
        yield None

    if write:
      sqliteConnection.commit()

    sqliteConnection.close()


"""
 Example
"INSERT INTO `records` (`time`, `pop_type`, `hom_result`) VALUES (%s, %s, %s)"
"""

# change this to add to database
def add_to_db(pee_or_poo = False, hit_or_miss=False):
    """Add chosen recipe to the shopping list"""
    with connect_to_db(write=True) as cursor:
      if cursor:
          # Write to database
          print("Writing to database")
          if not pee_or_poo:
              print("You need to specify if it was a pee or poo")
          else:
              now = datetime.now()
              now_str = now.strftime("%d/%m/%Y %H:%M:%S")
              query = f"INSERT INTO `records` (`time`, `pop_type`, `hom_result`) VALUES ('{now_str}', '{pee_or_poo.value}', '{hit_or_miss.value}')"
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
  add_to_db(PEE_POO_CLOCKED.PEE, HIT_OR_MISS.HIT)
  return goto_mainpage()


@app.route("/kiss_miss/")
def add_kiss_miss():
  add_to_db(PEE_POO_CLOCKED.PEE, HIT_OR_MISS.MISS)
  return goto_mainpage()


@app.route("/kiss_mix/")
def add_kiss_mixed_success():
    add_to_db(PEE_POO_CLOCKED.PEE, HIT_OR_MISS.MIXED_SUCCESS)
    return goto_mainpage()


@app.route("/bajs/")
def add_bajs():
  return render_template("bajs.html")


@app.route("/bajs_hit/")
def add_bajs_hit():
  add_to_db(PEE_POO_CLOCKED.POO, HIT_OR_MISS.HIT)
  return goto_mainpage()


@app.route("/bajs_miss/")
def add_bajs_miss():
  add_to_db(PEE_POO_CLOCKED.POO, HIT_OR_MISS.MISS)
  return goto_mainpage()


@app.route("/bajs_mix/")
def add_bajs_mixed_success():
    add_to_db(PEE_POO_CLOCKED.POO, HIT_OR_MISS.MIXED_SUCCESS)
    return goto_mainpage()


@app.route("/rutin/")
def add_rutin():
  return render_template("rutin.html")


@app.route("/rutin_hit/")
def add_rutin_hit():
    add_to_db(PEE_POO_CLOCKED.CLOCKED, HIT_OR_MISS.HIT)
    return goto_mainpage()


@app.route("/rutin_miss/")
def add_rutin_miss():
    add_to_db(PEE_POO_CLOCKED.CLOCKED, HIT_OR_MISS.MISS)
    return goto_mainpage()


@app.route("/")
def home():
  """Home page. Redirects to start screen"""
  return mainpage()

@app.route("/base/")
def mainpage():
    """
    Show the main page. A lot of data mangling happens here.
    Accessible via menu bar.
    """
    records = []
    db = {}
    if not os.path.exists(db_path):
        print("Could not find db. Populating new one")
        with connect_to_db(write=True) as cursor:
          # Create records table
          sql_create_records_table = """ CREATE TABLE IF NOT EXISTS records (
                                         time text PRIMARY KEY,
                                         pop_type text NOT NULL,
                                         hom_result text NOT NULL
                                     ); """
          cursor.execute(sql_create_records_table)

    with connect_to_db(write=False) as cursor:
      query = "SELECT * FROM records"
      result = cursor.execute(query)
      entries = result.fetchall()
      for res in entries:
        (day,time_stamp)  = res[0].split(' ')
        entry = (time_stamp, res[1], res[2])
        if day not in db.keys():
          db[day] = [entry]
        else:
          db[day].append(entry)

    for key, value in db.items():
        hits = 0
        entries = len(value)
        for (date, pee_or_poo, hit_or_miss) in value:
            if int(hit_or_miss) == HIT_OR_MISS.HIT.value:
                # All hits count. This doesn't inclue mixed successes since
                # they leave room for improvement.
                hits += 1
            elif int(pee_or_poo) == PEE_POO_CLOCKED.CLOCKED.value:
               # Special calculations for clocked (rutin) events.
               # If it is a hit, we count it as a hit in the previous if-statement.
               # If it is a miss, we don't the entry since we started it, but it failed.
               entries -= 1
        percent_hits = ceil(100*hits/entries)
        db[key] = (value, percent_hits, entries)

    # db is: ([entries], % hits, number of entries for day)
    return render_template("main.html", entries=db)


import os
db_path = '/var/lib/kissbajs/kissdagbok/kissochbajs.db'

def main(ip="0.0.0.0"):
    """Start the application. Entry point for the flask application"""
    # Load or create database
    
    # Start application
    app.run(debug=False, host=ip, port=5000)


if __name__ == "__main__":
    main()
