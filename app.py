import flask
import os
import json
import pandas as pd
from flask import Flask, render_template, request, current_app
from flask_pymongo import PyMongo
from src.utils import *
from src.graphics import stacked_bar_fig, pie_fig, line_fig, top_table
from src.movie_search_queries import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_ROOT_USER = os.getenv("MONGO_ROOT_USER")
MONGO_ROOT_PASSWORD = os.getenv("MONGO_ROOT_PASSWORD")
MONGO_URI = f"mongodb://{MONGO_ROOT_USER}:{MONGO_ROOT_PASSWORD}@mongo:27017/movies?authSource=admin"

mongo = PyMongo(app, uri=MONGO_URI)

@app.route("/", methods=["GET", "POST"])
def readme():
    return render_template("readme.html")

@app.route("/graphics", methods=["GET", "POST"])
def graphics():
    """Generates the graphics page, a page with graphs and tables illustrating information about the 
       selected dataset
    """
    country = request.form["country"] if "country" in request.form else ""
    is_movie = (
        request.form["movieOrSeries"] == "movie"
        if "movieOrSeries" in request.form
        else ""
    )
    is_series = (
        request.form["movieOrSeries"] == "series"
        if "movieOrSeries" in request.form
        else ""
    )
    years = request.form.getlist("movieYear") if "movieYear" in request.form else ""

    query = {
        **country_query(country=country),
        **year_query(years=years),
        **type_query(is_movie=is_movie, is_series=is_series),
    }

    find_movies = mongo.db.movies.find(query)
    df = pd.DataFrame(list(find_movies))

    pieGraphJSON = pie_fig(df, ["genres", "count"])
    lineGraphJSON = line_fig(df, ["year", "count"])
    stackedBarJSON = stacked_bar_fig(df, ["director", "wins", "nominations"])
    topTableJSON = top_table(df, ["title", "wins", "nominations"])

    return render_template(
        "graphics.html",
        pieGraphJSON=pieGraphJSON,
        lineGraphJSON=lineGraphJSON,
        stackedBarJSON=stackedBarJSON,
        topTableJSON=topTableJSON,
    )

@app.route("/movie_search", methods=["GET", "POST"])
def movie_search():
    """Generates the movie search page, where one can look up movies based on certain criteria
    """
    title = request.form["movieTitle"] if "movieTitle" in request.form else ""

    is_movie = "movieCheck" in request.form
    is_series = "seriesCheck" in request.form

    years = request.form.getlist("movieYear") if "movieYear" in request.form else ""

    query = {
        **title_query(title=title),
        **year_query(years=years),
        **type_query(is_movie=is_movie, is_series=is_series),
    }

    page, per_page, offset = get_page_items(request=request, current_app=current_app)

    movies_search = mongo.db.movies.find(query, {"_id": 0}).skip(offset).limit(per_page)
    num_of_movies = mongo.db.movies.find(query, {"_id": 0}).count()

    pagination = get_pagination(
        page=page,
        per_page=per_page,
        total=num_of_movies,
        record_name=movies_search,
        current_app=current_app,
    )

    return render_template(
        "movie_search.html",
        movies_search=movies_search,
        num_of_movies=num_of_movies,
        pagination=pagination,
    )


if __name__ == "__main__":
    app.run(debug=True)
