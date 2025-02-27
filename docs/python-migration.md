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

