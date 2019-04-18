import pytest


def test_home_page(test_client, database):
    response = test_client.get("/")
    assert response.status_code == 200

    # load recipes
    assert b"espresso" in response.data
    assert b"americana" in response.data
    assert b"cappuccino" in response.data
    assert b"latte" in response.data
    assert b"mokka" in response.data

    # load ingredients
    assert b"chocolade" in response.data
    assert b"coffe" in response.data
    assert b"foamed_milk" in response.data
    assert b"milk" in response.data
    assert b"water" in response.data
    assert b"whipped_cream" in response.data


def test_refill(test_client, database, ingredient, order):
    response = test_client.post("/refill")
    assert response.status_code == 302

    ingredients = ingredient.query.all()
    for ing in ingredients:
        assert ing.capacity == 1000


@pytest.mark.parametrize(
    "coffe,cost",
    [
        ("espresso", {"water": 50, "coffe": 50}),
        ("americana", {"water": 100, "coffe": 50}),
        ("cappuccino", {"water": 50, "coffe": 50, "milk": 50, "foamed_milk": 50}),
        ("latte", {"water": 50, "coffe": 50, "milk": 100}),
        ("mokka", {"water": 50, "coffe": 50, "chocolade": 50, "whipped_cream": 50}),
    ],
)
def test_coffe(test_client, database, ingredient, coffe, cost):

    # refill all ingredients
    response = test_client.post("/refill")
    assert response.status_code == 302

    response = test_client.post("/coffe", data={"coffe": coffe}, follow_redirects=True)

    assert response.status_code == 200
    assert bytes("Enjoy your {}".format(coffe), "utf-8") in response.data

    # check ingredient state after order
    for k, v in cost.items():
        ing = ingredient.query.filter_by(ingredient_name=k).first()
        assert ing.capacity == 1000 - v


def test_no_ingredients(test_client, database, ingredient):

    # refill all ingredients
    response = test_client.post("/refill")
    assert response.status_code == 302

    # clear the stock
    for ing in ingredient.query.all():
        ing.take_from_depot(20)

    response = test_client.post(
        "/coffe", data={"coffe": "espresso"}, follow_redirects=True
    )

    assert response.status_code == 200
    assert bytes("Refill ingredients to make coffe", "utf-8") in response.data

    # refill all ingredients
    response = test_client.post("/refill")
    assert response.status_code == 302
