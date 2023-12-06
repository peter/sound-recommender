# Sound Recommender

Basic song metadata CRUD API with playlists and recommendations based on playlists. Implemented using [FastAPI](https://fastapi.tiangolo.com) and Postgres + pgvector with OpenAI embeddings for recommendations.

## Limitations/Scope/Discussion

* Using OpenAPI embeddings as the recommendation engine may not be ideal (the vectors are quite large and the recommendations not super strong) but at least it's an easy way to get basic recommendation support. As an alternative to using an LLM (Large Language Model) we could have matched just on words and/or have come up with our own algorithm for sound distance that may or may not have worked better. However, such an approach would have been limited in that it does not necessarily have the semantic knowledge/relationship of words that an LLM does (i.e. which genres/artists are related etc.).
* The original Postman collection only created a single sound and since my recommendation endpoint wont return the sounds that recommendation is based on it would return an empty response and the Postman collection would fail. I fixed this by making the Postman collection create two sounds.
* I did not have time to implement any unit or system/http level tests (other than the Postman test collection)
* We do not check that sound IDs in playlists actually exist (no referential integrity there)
* I did not have time to add linting or type checking or automatic code formatting

## How to Evaluate this System without too much Installation

Since it can be tedious/difficult to install the dependencies for this system (you need Postgres + pgvector and an OpenAI API key) you can optionally evaulate it [on Heroku](https://sound-recommender-4853b1ecaf72.herokuapp.com).

In addition, if you remove the `openai_embedding` parts from the [sound model](src/models/sound.py) (i.e. lines 16 and 51) then you should be able to use all endpoints except the recommender endpoint (you will still need Postgres but you won't need pgvector or OpenAI).

## Development Setup (Local Installation)

Dependencies:

* Python (tested with 3.11.6)
* Postgres (tested with PostgreSQL 15 using [Postgres.app](https://postgresapp.com/) on Mac)
* The [pgvector extension](https://github.com/pgvector/pgvector) for embeddings
* An OpenAI API token in the environment variable `OPENAI_API_KEY`

Set up virtual environment and install Python libraries:

```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

If you are using Postgres.app on Mac then the pgvector installation should look something like this:

```sh
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
export PG_CONFIG=/Applications/Postgres.app/Contents/Versions/latest/bin/pg_config
# NOTE: need to permit terminal in Mac to modify add/delete other apps
sudo --preserve-env=PG_CONFIG make install
# You can check the .so file is installed here:
ls -l /Applications/Postgres.app/Contents/Versions/15/lib/postgresql
# You should now be able to run 'CREATE EXTENSION vector;' in your Postgres database, see below
```

Make sure you have Postgres installed and running locally and create the database and the pgvector extension:

```sh
createdb -U postgres sound-recommender
psql -U postgres sound-recommender -c 'CREATE EXTENSION vector;'
```

Run the migration to create the database tables:

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

## Test Data for Recommendations

To test the strength of recommendations I used a [Spotify dataset from Kaggle](https://www.kaggle.com/datasets/iamsumat/spotify-top-2000s-mega-dataset) that can be ingested with this script:

```sh
bin/ingest-test-data
```

## Invoking the API with Curl

```sh
export BASE_URL=http://localhost:8080

# Admin sounds create - Stairway to Heaven / Led Zeppelin
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Stairway to Heaven","genres":["rock"],"credits":[{"name":"Led Zeppelin","role":"ARTIST"}],"bpm":82}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Halo / Beyonce
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Halo","genres":["dance pop"],"credits":[{"name":"Beyonce","role":"ARTIST"}],"bpm":80}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Blank Space / Taylor Swift
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Blank Space","genres":["pop"],"credits":[{"name":"Taylor Swift","role":"ARTIST"}],"bpm":96}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Hips Don't Lie / Shakira Featuring Wyclef Jean
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Hips Dont Lie","genres":["latin pop","reggaeton"],"credits":[{"name":"Shakira Featuring Wyclef Jean","role":"ARTIST"}],"bpm":100}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Wrecking Ball / Miley Cyrus
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Wrecking Ball","genres":["pop"],"credits":[{"name":"Miley Cyrus","role":"ARTIST"}],"bpm":120}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Livin' La Vida Loca / Ricky Martin
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Livin La Vida Loca","genres":["latin pop","dance"],"credits":[{"name":"Ricky Martin","role":"ARTIST"}],"bpm":178}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Single Ladies (Put A Ring On It) / Beyonce
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Single Ladies (Put A Ring On It)","genres":["dance pop","r&b"],"credits":[{"name":"Beyonce","role":"ARTIST"}],"bpm":97}]}' $BASE_URL/admin/sounds | jq

# Admin sounds create - Master of Puppets / Metallica
curl -s -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Master of Puppets","genres":["thrash metal"],"credits":[{"name":"Metallica","role":"ARTIST"}],"bpm":220}]}' $BASE_URL/admin/sounds | jq

# Get sounds
curl -s $BASE_URL/sounds/1 | jq

# List sounds
curl -s $BASE_URL/sounds | jq

# List sounds by metallica
curl -s $BASE_URL/sounds?query=metallica | jq

# Admin sounds update
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Stairway to Hell","genres":["death metal"],"credits":[{"name":"Jakob Marklund","role":"ARTIST"}]}' $BASE_URL/admin/sounds/1

# Create playlist
curl -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Greatest of all time", "sounds":[1]}]}' $BASE_URL/playlists

# Get playlist
curl -s $BASE_URL/playlists/1 | jq

# List playlist
curl -s $BASE_URL/playlists | jq

# Update playlist
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Greatest of all time!!!", "sounds":[1]}' $BASE_URL/playlists/1

# Get playlist
curl -s $BASE_URL/playlists/1 | jq

# Get recommendations
curl -s $BASE_URL/sounds/recommended?playlistId=1 | jq

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

# Add Postgres with pgvector support
heroku addons:create heroku-postgresql:standard-0

# See status of Postgres addon
heroku addons

# Enable pgvector extension
heroku pg:psql -c 'CREATE EXTENSION vector'

# Deploy
git push heroku main

# Create the Postgres schema
heroku run bin/schema-migrate

# Check the database on Heroku with psql
heroku pg:psql

# See info about your database
heroku pg:info

# Add the OPENAI_API_KEY environment variable
heroku config:set OPENAI_API_KEY=...
heroku config

# Open the docs
heroku open

# Create a sound
export BASE_URL=https://sound-recommender-4853b1ecaf72.herokuapp.com
curl -i -H "Content-Type: application/json" -X POST -d '{"data":[{"title":"Stairway to Heaven","genres":["pop"],"credits":[{"name":"Led Zeppelin","role":"ARTIST"}]}]}' $BASE_URL/admin/sounds

# List sounds
curl -s $BASE_URL/sounds | jq

# Run postman tests
BASE_URL=https://sound-recommender-4853b1ecaf72.herokuapp.com bin/test-postman

# Ingest test data
BASE_URL=https://sound-recommender-4853b1ecaf72.herokuapp.com bin/ingest-test-data
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

* [pgvector](https://github.com/pgvector/pgvector)
* [pgvector-python](https://github.com/pgvector/pgvector-python)
* [pgvector support on Heroku](https://blog.heroku.com/pgvector-launch)
* [pgvector: Fewer dimensions are better](https://supabase.com/blog/fewer-dimensions-are-better-pgvector)
* [Chroma - Vector Database](https://github.com/chroma-core/chroma)
* [sqlite-vss](https://github.com/asg017/sqlite-vss)
* [Cosine Similarity vs Euclidian Distance](https://www.linkedin.com/pulse/similarity-measures-data-science-euclidean-distance-cosine-wynn#:~:text=Cosine%20similarity%20is%20generally%20preferred,of%20them%20vary%20by%20length.)

Song Metadata:

* [Spotify - All Time Top 2000s Mega Dataset](https://www.kaggle.com/datasets/iamsumat/spotify-top-2000s-mega-dataset)
* [Most Streamed Spotify Songs 2023](https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023)
* [Billboard top 100 Song/Artist](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs/data)
* [FMA: A Dataset For Music Analysis](https://github.com/mdeff/fma)

Alternatives to FastAPI for CRUD APIs with OpenAPI support in Python:

* [Python Example CRUD API (with OpenAPI/Validation)](https://github.com/peter/python-content-api)
