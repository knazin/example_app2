import datetime
from app import db

subs = db.Table(
    "recipe_ingredient",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.recipe_id")),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredient.ingredient_id")),
)


class Ingredient(db.Model):
    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String, unique=True)
    unit = db.Column(db.Float)
    capacity = db.Column(db.Float)

    def __init__(self, ingredient_name, unit, capacity):
        self.ingredient_name = ingredient_name
        self.unit = unit
        self.capacity = capacity


class Recipe(db.Model):
    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String, unique=True)
    portions = db.Column(db.String)
    ingredients = db.relationship(
        "Ingredient", secondary=subs, backref=db.backref("partsof", lazy="dynamic")
    )

    def __init__(self, recipe_name, ingredient_list, portions):
        self.recipe_name = recipe_name
        self.ingredients = ingredient_list
        self.portions = portions


class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(26))
    recipe_name = db.Column(
        db.String, db.ForeignKey("recipe.recipe_name"), nullable=False
    )

    def __init__(self, recipe_name):
        self.date = datetime.datetime.now().isoformat()
        self.recipe_name = recipe_name