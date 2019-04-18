def test_init_ingredient(ingredient):
    ing = ingredient("name", 50, 1000)
    assert ing.ingredient_name == "name"
    assert ing.unit == 50
    assert ing.capacity == 1000


def test_init_recipe(ingredient, recipe):
    ing = ingredient("name", 50, 1000)
    rec = recipe("recipe", [ing], "1")
    assert rec.recipe_name == "recipe"
    assert rec.ingredients[0].ingredient_name == "name"
    assert rec.portions == "1"


def test_init_order(ingredient, recipe, order):
    ord1 = order("recipe")
    assert ord1.recipe_name == "recipe"