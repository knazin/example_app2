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

@app.route("/coffe", methods=["POST"])
def coffe():
    coffe_name = request.form["coffe"]

    order = Order(coffe_name)
    done = order.make_coffe()

    if done:
        message = "Enjoy your {}".format(coffe_name)
        photo = coffe_name + ".jpg"
    else:
        message = "Refill ingredients to make coffe"
        photo = ""

    return redirect(url_for("index", message=message, photo=photo))


@app.route("/refill", methods=["POST"])
def refill():

    # refill all Ingredients
    [i.refill() for i in Ingredient.query.all()]

    return redirect(url_for("index", message="Refilled all Ingredients"))