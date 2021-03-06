import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import psycopg2
from app import app, db
from app.models import Ingredient, Recipe, Order

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


@pytest.fixture(scope="module")
def test_client():
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="module")
def database():
    yield db


@pytest.fixture(scope="module")
def ingredient():
    yield Ingredient


@pytest.fixture(scope="module")
def recipe():
    yield Recipe


@pytest.fixture(scope="module")
def order():
    yield Order
