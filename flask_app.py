"""
Flask application

The main page just re-directs to /recipes since that is
the most relevant page anyway. And who wants a 'Welcome here' page anyway?
"""
import os
import re
from copy import deepcopy
from flask import Flask, render_template, request
from enum import Enum
from time import *

import sqlite3

app = Flask(__name__)

class PEE_OR_POO(Enum):
    PEE = 1
    POO = 2

class HIT_OR_MISS(Enum):
  HIT = 1
  MISS = 2


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
              if hit_or_miss == HIT_OR_MISS.HIT:
                # Add PEE + HIT to SQL database
                print("PEE HIT")
              else:
                # Add PEE + MISS to SQL database
                print("PEE MISS")
            else:
              if hit_or_miss == HIT_OR_MISS.HIT:
                # Add POO + HIT to SQL database
                print("POO HIT")
              else:
                # Add POO + MISS to SQL database
                print("POO MISS")
    else:
        print("Failed to connect to database.")
    
@app.route("/kiss/")
def add_kiss():
  return render_template("kiss.html")

@app.route("/kiss_hit/")
def add_kiss_hit():
  # Add to database
  add_to_db(PEE_OR_POO.PEE, HIT_OR_MISS.HIT)
  return render_template("base.html")

@app.route("/kiss_miss/")
def add_kiss_miss():
  add_to_db(PEE_OR_POO.PEE, HIT_OR_MISS.MISS)
  return render_template("base.html")

@app.route("/bajs/")
def add_bajs():
  add_to_db(PEE_OR_POO.POO, HIT_OR_MISS.HIT)
  return render_template("bajs.html")

@app.route("/bajs_hit/")
def add_bajs_hit():
  add_to_db(PEE_OR_POO.POO, HIT_OR_MISS.MISS)
  return render_template("base.html")

@app.route("/bajs_miss/")
def add_bajs_miss():
  print("BAJS MISS")
  return render_template("base.html")

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
#    read from cursor
    return render_template("base.html")


def main(ip="0.0.0.0"):
    """Start the application. Entry point for the flask application"""
    # Load or create database

    # Start application
    app.run(debug=False, host=ip)


if __name__ == "__main__":
    main()
