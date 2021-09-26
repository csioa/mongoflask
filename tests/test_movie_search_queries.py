from src.movie_search_queries import *


def test_title_query():
    assert bool(title_query("")) == False
    assert title_query(title="Braveheart") == {
        "title": {"$regex": "Braveheart", "$options": "i"}
    }


def test_country_query():
    assert bool(country_query("")) == False
    assert country_query(country="USA") == {
        "country": {"$regex": "USA", "$options": "i"}
    }


def test_type_query():
    assert bool(type_query(is_movie=True, is_series=True)) == False
    assert type_query(is_movie=True, is_series=False) == {"type": "movie"}
    assert type_query(is_movie=False, is_series=True) == {"type": "series"}
    assert type_query(is_movie=False, is_series=False) == {"type": "other"}


def test_year_query():
    assert bool(year_query("")) == False
    assert year_query(["2000", "2015"]) == {"year": {"$in": [2000, 2015]}}
