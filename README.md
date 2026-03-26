# Flask App Blueprint: the fast way to start your MVP
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jelmerdejong/flask-app-blueprint?quickstart=1)

Flask App Blueprint is a small starter app for Flask 3 projects. It includes authentication, CRUD examples, database migrations, transactional email hooks, a verified unittest suite, and a workflow that works locally, in GitHub Codespaces, and on Heroku.

## Features
* User registration, email confirmation, and password reset via SMTP
* User profiles, including change password
* Admin only pages including statistics and user management
* Public and member only pages
* Database setup, including database migrations and CRUD examples
* Local development with SQLite by default, optional PostgreSQL, and Heroku deployment support
* GitHub Codespaces support through a checked-in devcontainer
* Powerful stack: back-end based on Python with Flask, front-end is Bootstrap `5.3.8` with the Bootstrap bundle JS
* Including basic test coverage with Python's built-in `unittest` framework

## Quick Start
1. Install `uv`: `python -m pip install uv`
2. Sync the locked environment: `uv sync --locked`
3. Copy `.env.example` to `.env` if you want to set a real `SECRET_KEY`, PostgreSQL, or SMTP credentials
4. Apply migrations: `uv run flask db upgrade`
5. Run tests: `uv run python -m unittest discover -s project/tests -v`
6. Start the app: `uv run flask run`

## Documentation
Find all the documentation in this repository in the [docs folder](docs/README.md).

### [Getting Started](docs/getting-started.md)
