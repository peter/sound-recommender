# Sound Recommender

## Development Setup

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

* [Python Example CRUD API (with OpenAPI/Validation)](https://github.com/peter/python-content-api)
