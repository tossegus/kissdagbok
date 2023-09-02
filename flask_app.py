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

app = Flask(__name__)

class PEE_OR_POO(Enum):
    PEE = 1
    POO = 2

class HIT_OR_MISS(Enum):
  HIT = 1
  MISS = 2

# change this to add to database
def add_to_shoppinglist(pee_or_poo = False, hit_or_miss=False):
    """Add chosen recipe to the shopping list"""
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

@app.route("/kiss/")
def add_kiss():
  print("KISS")
  return render_template("kiss.html")

@app.route("/kiss_hit/")
def add_kiss_hit():
  print("KISS HIT")
  # Add to database
  return render_template("base.html")

@app.route("/kiss_miss/")
def add_kiss_miss():
  print("KISS MISS")
  return render_template("base.html")


@app.route("/bajs/")
def add_bajs():
  print("BAJS")
  return render_template("bajs.html")

@app.route("/bajs_hit/")
def add_bajs_hit():
  print("BAJS HIT")
  # Add to database
  return render_template("base.html")

@app.route("/bajs_miss/")
def add_bajs_miss():
  print("BAJS MISS")
  return render_template("base.html")

@app.route("/")
def home():
  """Home page. Redirects to recipes page"""
  return mainpage()

record = {}

@app.route("/base/")
def mainpage():
    """
    Show the recipes page. A lot of data mangling happens here.
    Accessible via menu bar.
    """
    # Connect to database
    # Make sure to render add event with a link to next page with KISS/BAJS
    # Add that to a global dictionary with {pee/poo: hit/miss} that should be added to the database with a timestamp
    # On next page add TRÄFF eller MISS
    return render_template("base.html")


@app.route("/shoppinglist/", methods=["POST", "GET"])
def shoppinglist():
    """
    Show the Shopping List page. This page is empty if no recipes have
    been added in recipes view.
    Accissble via menu bar.
    """
    global shopping_list
    if request.method == "POST":
        CMD = request.form.get("button")
        if CMD == "clear_list":
            shopping_list = []
        elif CMD in shopping_list:
            shopping_list.remove(CMD)

    int_dict = {}

    if not shopping_list:
        # The shopping_list is empty
        print("Empty list")
    else:
        print("List not empty")
        for item in shopping_list:
            filename = os.path.basename(item)
            int_dict[filename] = item
        print("List is not empty")
    return render_template("shopping_list.html", recipes=int_dict)


@app.route("/printshoppinglist/", methods=["POST", "GET"])
def printshoppinglist():
    """
    Displays the items in the shopping list.
    Only available through Shopping List
    """
    global shopping_list
    int_shoppinglist = ShoppingList()
    int_dict = {}
    if request.method == "POST":
        if request.form.get("button") == "empty_list":
            shopping_list = []
    else:
        if not shopping_list:
            print("Shopping list empty")
        else:
            for item in shopping_list:
                int_shoppinglist.add_recipe(parseRecipe(item))

        for item in int_shoppinglist.items:
            int_dict[item] = (
                f"{int_shoppinglist.items[item].quantity}"
                + f"{int_shoppinglist.items[item].unit}"
            )

    return render_template("print_shopping_list.html", shoppinglist=int_dict)


@app.route("/recipe/", methods=["POST", "GET"])
def recipe():
    """Recipe page. Show the selected recipe."""
    path = request.args.get("recipe_path")
    recipe_name = os.path.basename(path).replace(".cook", "")
    if request.method == "POST":
        print("Got button press!")
        if request.form.get("add_to_recipe") == "add":
            # add this recipe to the shopping_list
            add_to_shoppinglist(path)

    else:
        path = request.args.get("recipe_path")

    int_recipe = Recipe(path)
    ingredients = []
    for item in int_recipe.ingredients:
        quantity = convert_str_to_float(item["quantity"])
        ingredients.append(f'{item["name"]} {quantity}{item["units"]}')

    step_list = int_recipe.steps_str.split("\n")
    step_dict = {}
    for item in step_list:
        if match := re.search("[^ ]", item):
            index = match.start()
        else:
            index = 0
        # Strip leading white spaces
        key = item[index:]
        step_dict[key] = "TAB" if key.startswith("[") else "BASE"

    return render_template(
        "recipe.html",
        path=path,
        recipe_name=recipe_name,
        metadata=int_recipe.metadata,
        ingredients=ingredients,
        steps=step_dict,
    )


def main(ip="0.0.0.0"):
    """Start the application. Entry point for the flask application"""
    # Start application
    app.run(debug=False, host=ip)


if __name__ == "__main__":
    main()
