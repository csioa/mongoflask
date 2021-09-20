import flask
import os
from flask import Flask, render_template, request, current_app
from flask_pymongo import PyMongo
from src.utils import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_ROOT_USER = os.getenv("MONGO_ROOT_USER")
MONGO_ROOT_PASSWORD = os.getenv("MONGO_ROOT_PASSWORD")
MONGO_URI = f"mongodb://{MONGO_ROOT_USER}:{MONGO_ROOT_PASSWORD}@mongo:27017/movies?authSource=admin"

mongo = PyMongo(app, uri=MONGO_URI)

def title_query(title):
    query = {}
    if not title:
        return query
    query['title'] = {'$regex' : title, '$options' : 'i'}
    return query

def type_query(is_movie, is_series):
    query = {}
    if is_movie and is_series:
        return query
    elif is_movie and not is_series:
        query['type'] = 'movie'
    elif is_series:
        query['type'] = 'series'
    else:
        query['type'] = 'other'
    print(query, flush=True)
    return query

def year_query(years):
    if not years:
        return {}
    years = [int(year) for year in years]
    return {'year': {'$in': years} }

@app.route('/readme')
def hello():
    return render_template("readme.html")

@app.route('/movie_list', methods=['GET','POST'])
def movie_list():

    title = request.form['movieTitle']

    is_movie = 'movieCheck' in request.form
    is_series = 'seriesCheck' in request.form

    years = request.form.getlist('movieYear') if 'movieYear' in request.form else ''

    query = {
        **title_query(title=title),
        **year_query(years=years),
        **type_query(is_movie=is_movie, is_series=is_series)
    }

    page, per_page, offset = get_page_items(request=request, current_app=current_app)
    movies_search = mongo.db.movies.find(query, {'_id': 0}).skip(offset).limit(per_page)
    num_of_movies = mongo.db.movies.find(query, {'_id': 0}).count()

    pagination = get_pagination(page=page,
                per_page=per_page,
                total=num_of_movies,
                record_name=movies_search,
                current_app=current_app
                )

    return render_template('movie_search.html',
                            movies_search=movies_search,
                            num_of_movies=num_of_movies,
                            pagination=pagination)

if __name__ == '__main__':
    app.run(debug=True)