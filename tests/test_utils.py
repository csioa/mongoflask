from src.utils import *
from flask import Flask, request
from flask_paginate import Pagination

app = Flask('app')

def test_get_css_framework():
    assert get_css_framework(app) == 'bootstrap4'

def test_get_link_size():
    assert get_link_size(app) == 'sm'

def test_show_single_page_or_not():
    assert show_single_page_or_not(app) == False

def test_get_page_items():
    with app.test_request_context('/?page=1&per_page=20'):
        assert get_page_items(request, app) == (1, 20, 0)

def test_get_pagination():
    assert get_pagination(app) == Pagination(
        css_framework='bootstrap4',
        link_size='sm',
        show_single_page=False,
        **kwargs
    )