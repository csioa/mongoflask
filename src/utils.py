import os
from flask_paginate import Pagination
from dotenv import load_dotenv

load_dotenv()  

PAGE_ITEMS = os.getenv("PAGE_ITEMS")

def get_css_framework(current_app):
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap4')


def get_link_size(current_app):
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not(current_app):
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_page_items(request, current_app):
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
            per_page = current_app.config.get('PER_PAGE', int(PAGE_ITEMS))
    else:
            per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(current_app, **kwargs):
       kwargs.setdefault('record_name', 'records')
       return Pagination(css_framework=get_css_framework(current_app=current_app),
          link_size=get_link_size(current_app=current_app),
          show_single_page=show_single_page_or_not(current_app=current_app),
          **kwargs
          )