# Technology Stack
* Runtime: Python `3.11` declared in [`.python-version`](../.python-version)
* Web framework: Flask `3.1`
* Front-end: Bootstrap `5.3.8` via CDN, using the Bootstrap bundle JS without jQuery
* ORM: SQLAlchemy `2.0` through Flask-SQLAlchemy `3.1`
* Forms: Flask-WTF and WTForms
* Authentication: Flask-Login and Flask-Bcrypt
* Email: Flask-Mail with SMTP configuration from environment variables
* Database migrations: Alembic via Flask-Migrate
* Local development database: SQLite by default
* Production database: PostgreSQL
* Dependency manager and lockfile: `uv` with `pyproject.toml` and `uv.lock`
* Process model: Gunicorn via [Procfile](../Procfile)
* Tests: Python `unittest`
* CI: CircleCI
* Cloud development: GitHub Codespaces via [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json)
* Deployment target: Heroku
