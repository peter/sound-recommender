# Sound Recommender

Basic song metadata CRUD API with playlists and recommendations based on playlists. Implemented using [FastAPI](https://fastapi.tiangolo.com).

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

# sounds create
curl -i -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Stairway to Heaven","genres":["pop"],"credits":[{"name":"Led Zeppelin","role":"ARTIST"}]}]}' $BASE_URL/admin/sounds

# sounds get
curl -i $BASE_URL/sounds/1

# sounds list
curl -i $BASE_URL/sounds

# sounds update

# sounds delete
```

## Heroku Deployment

The files [runtime.txt](runtime.txt) and [Procfile](Procfile) were added Python version and start command. Creating and deploying the app with the Heroku CLI:

```sh
# Create app
heroku apps:create sound-recommender --region eu

# Add Postgres
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Create the Postgres schema
heroku run python -c "import src.db.pg as pg; pg.connect(); pg.create_schema()"

# Open the docs
heroku open
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

* [FastAPI - Getting Started](https://fastapi.tiangolo.com/#installation)
* [Example FastAPI CRUD API with Postgres](https://github.com/jeremyleonardo/books-crud-fastapi)
* [SQLite in Python](https://docs.python.org/3.11/library/sqlite3.html)
* [Poetry - Dependency Management](https://python-poetry.org)
* [Build a CRUD API using FastAPI, Python, and SQLite For New Coders](https://blog.stackademic.com/how-to-build-a-crud-api-using-fastapi-python-sqlite-for-new-coders-2d056333ea20)

Heroku deployment:

* [gunicorn vs uvicorn](https://stackoverflow.com/questions/59391560/how-to-run-uvicorn-in-heroku)
* [Heroku Python getting started app](https://github.com/heroku/python-getting-started)
* [CREATE TABLE IF NOT EXISTS error - pg_class_relname_nsp_index](https://stackoverflow.com/questions/74261789/postgres-create-table-if-not-exists-%E2%87%92-23505)


Recommendations:

* [Chroma - Vector Database](https://github.com/chroma-core/chroma)
* [sqlite-vss](https://github.com/asg017/sqlite-vss)
* [pgvector](https://github.com/pgvector/pgvector)
* [Cosine Similarity vs Euclidian Distance](https://www.linkedin.com/pulse/similarity-measures-data-science-euclidean-distance-cosine-wynn#:~:text=Cosine%20similarity%20is%20generally%20preferred,of%20them%20vary%20by%20length.)

Alternatives to FastAPI for CRUD APIs with OpenAPI support in Python:

* [Python Example CRUD API (with OpenAPI/Validation)](https://github.com/peter/python-content-api)
