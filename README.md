# Simple Flask web app on top of MongoDB

[![Build Status](https://app.travis-ci.com/csioa/mongoflask.svg?branch=main)](https://app.travis-ci.com/csioa/mongoflask)
<img src="https://coveralls.io/repos/github/csioa/mongoflask/badge.svg?branch=main&kill_cache=1" />

### Importing data in MongoDB - movies collection 
```bash
mongoimport -u "<MONGO_ROOT_USER>" -p "<MONGO_ROOT_PASSWORD>" --authenticationDatabase "admin" --db movies --collection movies --file data/datasets/movies.json
```
### Sample .env file contains 
- MONGO_ROOT_USER=devroot
- MONGO_ROOT_PASSWORD=devroot
- MONGOEXPRESS_LOGIN=dev
- MONGOEXPRESS_PASSWORD=dev
- PAGE_ITEMS=30

### Getting started
```bash
docker compose --env-file .env up
```

### Home screen

```bash
http://localhost:5001
```

#### The home screen which has a small description and the available endpoints

![Home screen](images/home_screen.png)

#### The /movie_search endpoint will list movies according to the selected filters. If nothing is selected all movies will be listed.

![Movie search](images/movie_search.png)

#### The /graphics endpoint will show
- Number of movies per genre (pie chart)
- Number of movies per year (line graph)
- Number of award nomination/wins per director (stacked bar chart)
- List with the top 20 award winner and nominated movies

![Graphics](images/graphics.png)