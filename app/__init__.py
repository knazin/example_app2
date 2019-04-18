import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

if "DOCKER" in os.environ:
    DB_URI = os.environ["DATABASE_URI"]
else:
    DB_URI = os.environ["DATABASE_URI_LOCAL"]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from app import models, views
from app.models import Ingredient, Recipe, Order


def recreate_db():
    db.session.remove()
    db.reflect()
    db.drop_all()
    db.create_all()


def seed_db():
    # Link to Recipe
    # https://www.garneczki.pl/blog/10-najpopularniejszych-sposobow-podawania-kawy/

    # Add Ingredients

    water = Ingredient("water", 50, 1000)
    water.save_to_db()

    milk = Ingredient("milk", 50, 1000)
    milk.save_to_db()

    foamed_milk = Ingredient("foamed_milk", 50, 1000)
    foamed_milk.save_to_db()

    coffe = Ingredient("coffe", 50, 1000)
    coffe.save_to_db()

    chocolade = Ingredient("chocolade", 50, 1000)
    chocolade.save_to_db()

    whipped_cream = Ingredient("whipped_cream", 50, 1000)
    whipped_cream.save_to_db()

    # Add Recipes

    espresso = Recipe("espresso", [water, coffe], "1,1")
    espresso.save_to_db()

    americana = Recipe("americana", [water, coffe], "2,1")
    americana.save_to_db()

    cappuccino = Recipe("cappuccino", [water, milk, foamed_milk, coffe], "1,1,1,1")
    cappuccino.save_to_db()

    latte = Recipe("latte", [water, milk, coffe], "1,2,1")
    latte.save_to_db()

    mokka = Recipe("mokka", [water, coffe, chocolade, whipped_cream], "1,1,1,1")
    mokka.save_to_db()
