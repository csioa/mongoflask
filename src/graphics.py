import json
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def pie_fig(df: pd.DataFrame, columns:list) -> str:
    """Prepares the object for illustrating a pie chart on movies per genre
    based on the search criteria

    Args:
        df (pd.DataFrame): input DataFrame after search filters are applied
        columns (list): list of column names of the expected DataFrame

    Returns:
        str: A JSON encoded string
    """
    if not df.empty:
        genres_count = (
            df.explode("genres")
            .groupby(["genres"])["_id"]
            .count()
            .reset_index(name="count")
        )
    else:
        genres_count = pd.DataFrame(columns=columns)

    genres_count = genres_count
    pie_fig = px.pie(
        genres_count, values="count", names="genres", title="Movies per Genre"
    )
    pieGraphJSON = json.dumps(pie_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return pieGraphJSON

def stacked_bar_fig(df: pd.DataFrame, columns:list) -> str:
    """Prepares the object for illustrating a stacked bar chart on wins and
    nominations of movies per director based on the search criteria

    Args:
        df (pd.DataFrame): input DataFrame after search filters are applied
        columns (list): list of column names of the expected DataFrame

    Returns:
        str: A JSON encoded string
    """
    if not df.empty and "directors" in list(df.columns):
        awards_nominations = df.explode("directors")[["directors", "awards"]]
        awards_nominations = (
            pd.json_normalize(json.loads(awards_nominations.to_json(orient="records")))
            .groupby("directors")
            .sum()
            .reset_index()
        )
        awards_nominations.columns = columns
    else:
        awards_nominations = pd.DataFrame(columns=columns)

    stacked_bar_fig = px.bar(
        awards_nominations.sort_values("wins", ascending=False).head(20),
        x="director",
        y=["wins", "nominations"],
        title="Nominations and Awards per Director",
    )
    stackedBarJSON = json.dumps(stacked_bar_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return stackedBarJSON

def line_fig(df: pd.DataFrame, columns:list) -> str:
    """Prepares the object for illustrating a line graph on number of
    movies per year based on the search criteria

    Args:
        df (pd.DataFrame): input DataFrame after search filters are applied
        columns (list): list of column names of the expected DataFrame

    Returns:
        str: A JSON encoded string
    """
    if not df.empty:
        num_of_movies_per_year = (
            df.groupby(["year"])["_id"].count().reset_index(name="count")
        )
    else:
        num_of_movies_per_year = pd.DataFrame(columns=columns)

    line_fig = px.line(
        num_of_movies_per_year, x="year", y="count", title="Movies per Year"
    )
    line_fig.update_layout(bargap=0.1)
    lineGraphJSON = json.dumps(line_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return lineGraphJSON

def top_table(df: pd.DataFrame, columns:list) -> str:
    """Prepares the object for illustrating a table with the top 20 movies
    and their nominations and wins sorted on descending order upon wins

    Args:
        df (pd.DataFrame): input DataFrame after search filters are applied
        columns (list): list of column names of the expected DataFrame

    Returns:
        str: A JSON encoded string
    """
    if not df.empty:
        num_of_awards_per_movie = (
            pd.json_normalize(
                json.loads((df[["title", "awards"]]).to_json(orient="records"))
            )
            .groupby("title")
            .sum()
            .reset_index()
        )
        num_of_awards_per_movie.columns = columns
    else:
        num_of_awards_per_movie = pd.DataFrame(columns=columns)

    num_of_awards_per_movie = num_of_awards_per_movie.sort_values(
        "wins", ascending=False
    ).head(20)

    top_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(num_of_awards_per_movie.columns),
                    fill_color="#636dfa",
                    font_color="white",
                    align="left",
                ),
                cells=dict(
                    values=[
                        num_of_awards_per_movie.title,
                        num_of_awards_per_movie.wins,
                        num_of_awards_per_movie.nominations,
                    ],
                    fill_color="lavender",
                    align="left",
                ),
            )
        ]
    )
    topTableJSON = json.dumps(top_table, cls=plotly.utils.PlotlyJSONEncoder)
    return topTableJSON