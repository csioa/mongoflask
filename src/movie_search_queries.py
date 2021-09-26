def title_query(title: str) -> dict:
    query = {}
    if not title:
        return query
    query["title"] = {"$regex": title, "$options": "i"}
    return query

def country_query(country: str) -> dict:
    query = {}
    if not country:
        return query
    query["country"] = {"$regex": country, "$options": "i"}
    return query

def type_query(is_movie: bool, is_series: bool) -> dict:
    query = {}
    if is_movie and is_series:
        return query
    elif is_movie and not is_series:
        query["type"] = "movie"
    elif is_series and not is_movie:
        query["type"] = "series"
    else:
        query["type"] = "other"
    return query

def year_query(years:str) -> dict:
    if not years:
        return {}
    years = [int(year) for year in years]
    return {"year": {"$in": years}}
