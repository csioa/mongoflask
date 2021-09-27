# Simple Flask web app on top of MongoDB

[![Build Status](https://app.travis-ci.com/csioa/mongoflask.png?branch=main)](https://app.travis-ci.com/csioa/mongoflask)
[![Coverage Status](https://coveralls.io/repos/github/csioa/mongoflask/badge.png?branch=main)](https://coveralls.io/github/csioa/mongoflask?branch=main)

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