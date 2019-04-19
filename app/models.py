import json
import datetime
from app import db

subs = db.Table(
    "recipe_ingredient",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.recipe_id")),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.ingredient_id")),
)


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String, unique=True)
    unit = db.Column(db.Float)
    capacity = db.Column(db.Float)

    def __init__(self, ingredient_name, unit, capacity):
        self.ingredient_name = ingredient_name
        self.unit = unit
        self.capacity = capacity

    def to_dict(self):
        return {
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient_name,
            "unit": self.unit,
            "capacity": self.capacity,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(ingredient_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_depot(self, portion):
        return self.capacity >= (self.unit * int(portion))

    def take_from_depot(self, portion):
        self.capacity -= self.unit * int(portion)
        db.session.commit()

    def refill(self):
        self.capacity = 1000
        db.session.commit()


class Recipe(db.Model):
    __tablename__ = "recipes"

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

    def to_dict(self):
        return {
            "recipe_id": self.recipe_id,
            "recipe_name": self.recipe_name,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(recipe_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(26))
    recipe_name = db.Column(
        db.String, db.ForeignKey("recipes.recipe_name"), nullable=False
    )

    def __init__(self, recipe_name):
        self.date = datetime.datetime.now().isoformat()
        self.recipe_name = recipe_name

    def make_coffe(self):
        # get recipe object of order
        recipe = Recipe.find_by_name(self.recipe_name)
        portions = json.loads(recipe.portions)

        # check ingredients of recipe in depots
        for ing in recipe.ingredients:
            if not ing.check_depot(portions[ing.ingredient_name]):
                return False

        # get ingredients from depots
        for ing in recipe.ingredients:
            ing.take_from_depot(portions[ing.ingredient_name])

        # save to db
        db.session.add(self)
        db.session.commit()

        return True