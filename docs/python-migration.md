# Notes on migrating to Python

## Setup

Installed pipx: 
```
sudo apt install pipx
```

Installed poetry:

```
pipx install poetry
pipx ensurepath
```

Initialise:

Create new terminal (for PATH change).
```
poetry init
```
Set project name to "query"

Add FastAPI
```
poetry add fastapi[standard]
```

Create main.py in query folder and paste in FastAPI example code.

Noticed VSCode not highlighting properly. Get poetry environment path with:
```
poetry env info --path
```
Then set this path using the "Python: Select Interpreter" command in VSCode

To run server:
```
poetry run fastapi dev --port 5513 query/main.py
```
Addded `**/__pycache__/` to .gitignore and .dockerignore

## Health Check

### PostgreSQL

Tried using pre-built one from: https://github.com/jtom38/fastapi_healthcheck_sqlalchemy but got into a bit of a rabbit hole with middleware and async support.

In the end started with a vary basic bit of code using the `asyncpg` driver.

### MongoDB

Using motor

## Debugging in VSCode

Added the following configuration to launch.json:

```json
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "fastapi",
            "args": [
                "dev",
                "--port",
                "5513",
                "query/main.py"
            ],
            "env": {
                "VAR": "Note need to set environment overrides here as .envrc is not read"
            },
            "jinja": true
        }
```

Note VSCode doesn't read `.envrc` but it does read `.env` into the environment which means you can't even load `.envrc` in main.py as the environment variables are already set and take precedence.

## Adding tests

Needed to install `pytest-asyncio` to test async methods

Note that again tests don't read `.envrc` but this is probably a good thing as they need to not be tied to the local environment.

## Tidy up dependencies

Remove `fastapi[standard]` and then re-added just `fastapi`. Added `uvicorn[standard]` as a normal dependency and then `fastapi-cli` as a dev-only dependency.

## Migrations

Decided to roll own to keep simple. Stick with same mikro_orm table.

## Testcontainers

This was relatively simple. Followed the docs: https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/

Main complication was mocking the health check to return an OK response for MongoDB but also had to change the fixture event loop to use session scope:https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_fixture_loop.rst


# Docker

Created a simple Dockerfile_python to run side-by-side with existing off-query.

Copied basic structure from taxonomy-editor but without the off user stuff.

# TODO

 - query services
 - redis import
 - incremental / full import
