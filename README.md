# Sound Recommender

Basic song metadata CRUD API with playlists and recommendations based on playlists. Implemented using [FastAPI](https://fastapi.tiangolo.com) and Postgres.

## Development Setup

Dependencies:

* Python (tested with 3.11.6)
* Postgres (tested with PostgreSQL 15 using Postgres.app on Mac)

Set up virtual environment and install dependencies:

```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Make sure you have Postgres installed and running locally and create the schema:

```sh
bin/schema-migrate
```

Start the server:

```sh
bin/start-dev
```

Running the Postman tests (requires first [installing the Postman CLI](https://learning.postman.com/docs/postman-cli/postman-cli-installation/)):

```sh
bin/test-postman
```

OpenAPI docs:

```sh
open http://localhost:8080/docs
```

OpenAPI spec:

```sh
open http://localhost:8080/openapi.json
```

## Invoking the API with Curl

```sh
export BASE_URL=http://localhost:8080

# Admin sounds create
curl -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Stairway to Heaven","genres":["pop"],"credits":[{"name":"Led Zeppelin","role":"ARTIST"}]}]}' $BASE_URL/admin/sounds | jq

# sounds get
curl $BASE_URL/sounds/1 | jq

# sounds list
curl $BASE_URL/sounds | jq

# Admin sounds update
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Stairway to Hell","genres":["death metal"],"credits":[{"name":"Jakob Marklund","role":"ARTIST"}]}' $BASE_URL/admin/sounds/1

# Create playlist
curl -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Greatest of all time", "sounds":[1]}]}' $BASE_URL/playlists

# List playlists
curl -s $BASE_URL/playlists/1 | jq

# Get playlist
curl -s $BASE_URL/playlists/1 | jq

# Update playlist
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Greatest of all time!!!", "sounds":[1]}' $BASE_URL/playlists/1

# Get playlist
curl -s $BASE_URL/playlists/1 | jq

# Delete playlist
curl -i -X DELETE $BASE_URL/playlists/1

# Admin sounds delete
curl -i -X DELETE $BASE_URL/admin/sounds/1
```

## Heroku Deployment

The files [runtime.txt](runtime.txt) and [Procfile](Procfile) and they contain the Python version and the start command. The following commands were used to create and deploy the app with the Heroku CLI:

```sh
# Create app
heroku apps:create sound-recommender --region eu

# Add Postgres
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Create the Postgres schema
heroku run bin/schema-migrate

# Check the database on Heroku with psql
heroku pg:psql

# Open the docs
heroku open

# Create a sound
export BASE_URL=https://sound-recommender-4853b1ecaf72.herokuapp.com
curl -i -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Stairway to Heaven","genres":["pop"],"credits":[{"name":"Led Zeppelin","role":"ARTIST"}]}]}' $BASE_URL/admin/sounds

# List sounds
curl -s $BASE_URL/sounds | jq
```

## Sound Schema

```json
{
    "title": "New song",
    "bpm": 120,
    "genres": [
        "pop"
    ],
    "duration_in_seconds": 120,
    "credits": [
        {
            "name": "King Sis",
            "role": "VOCALIST"
        },
        {
            "name": "Ooyy",
            "role": "PRODUCER"
        }
    ]
}
```

## Playlist Schema

```json
{
    "title": "New playlist",
    "sounds": [
        "{{soundId}}"
    ]
}
```

## Resources

Python libraries, tools, and examples:

* [FastAPI - Getting Started](https://fastapi.tiangolo.com/#installation)
* [Example FastAPI CRUD API with Postgres](https://github.com/jeremyleonardo/books-crud-fastapi)
* [SQLite in Python](https://docs.python.org/3.11/library/sqlite3.html)
* [Poetry - Dependency Management](https://python-poetry.org)
* [Build a CRUD API using FastAPI, Python, and SQLite For New Coders](https://blog.stackademic.com/how-to-build-a-crud-api-using-fastapi-python-sqlite-for-new-coders-2d056333ea20)
* [SQLAlchemy](https://www.sqlalchemy.org/)

Heroku deployment:

* [gunicorn vs uvicorn](https://stackoverflow.com/questions/59391560/how-to-run-uvicorn-in-heroku)
* [Heroku Python getting started app](https://github.com/heroku/python-getting-started)
* [CREATE TABLE IF NOT EXISTS error - pg_class_relname_nsp_index](https://stackoverflow.com/questions/74261789/postgres-create-table-if-not-exists-%E2%87%92-23505)


Recommendations:

* [Chroma - Vector Database](https://github.com/chroma-core/chroma)
* [sqlite-vss](https://github.com/asg017/sqlite-vss)
* [pgvector](https://github.com/pgvector/pgvector)
* [Cosine Similarity vs Euclidian Distance](https://www.linkedin.com/pulse/similarity-measures-data-science-euclidean-distance-cosine-wynn#:~:text=Cosine%20similarity%20is%20generally%20preferred,of%20them%20vary%20by%20length.)

Song Metadata:

* [Spotify - All Time Top 2000s Mega Dataset](https://www.kaggle.com/datasets/iamsumat/spotify-top-2000s-mega-dataset)
* [Most Streamed Spotify Songs 2023](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)
* [Billboard top 100 Song/Artist](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs/data)

Alternatives to FastAPI for CRUD APIs with OpenAPI support in Python:

* [Python Example CRUD API (with OpenAPI/Validation)](https://github.com/peter/python-content-api)
