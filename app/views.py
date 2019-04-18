from flask import render_template, url_for, redirect, request
from app import app, db
from app.models import Recipe, Ingredient, Order


@app.route("/")
def index():
    # prepare data for html template
    dane = {
        "recipes": [r.to_dict() for r in Recipe.query.all()],
        "ingredients": [
            i.to_dict()
            for i in Ingredient.query.order_by(Ingredient.ingredient_name).all()
        ],
        "message": "",
        "photo": "../static/img/",
    }

    # parse passed args - GUI
    if "message" in request.args:
        dane["message"] = request.args["message"]
    if "photo" in request.args:
        dane["photo"] = request.args["photo"]

    return render_template("index.htm", dane=dane)