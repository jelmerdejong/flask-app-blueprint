# Getting Started
This repository now targets a modern Flask workflow:

* Python `3.11` is the declared project runtime in [`.python-version`](../.python-version)
* Local development defaults to SQLite
* Tests run against an isolated temporary SQLite database
* Heroku deployment uses the checked-in `Procfile` plus `flask db upgrade`
* The UI uses Bootstrap `5.3.8` from CDN and no longer depends on jQuery

## 1. Local setup
1. Clone the repository and enter it:
   `git clone git@github.com:jelmerdejong/flask-app-blueprint.git`
   `cd flask-app-blueprint`
2. Install `uv`:
   `python -m pip install uv`
3. Sync the locked environment:
   `uv sync --locked`
4. Optional: create a local `.env` file from the checked-in example:
   `cp .env.example .env`
5. Apply database migrations:
   `uv run flask db upgrade`
6. Start the development server:
   `uv run flask run`

The app uses `sqlite:///app.db` by default. If you want to use PostgreSQL locally, set `DATABASE_URL` in `.env`.

## 2. Run the test suite
Run:

`uv run python -m unittest discover -s project/tests -v`

The test suite creates and tears down its own temporary SQLite database, so you do not need to provision a separate `test` database first.

## 3. Configure email
The app sends mail through `Flask-Mail`. Copy [`.env.example`](../.env.example) to `.env` and set the SMTP values you need:

* `MAIL_SERVER`
* `MAIL_PORT`
* `MAIL_USE_TLS`
* `MAIL_USE_SSL`
* `MAIL_USERNAME`
* `MAIL_PASSWORD`
* `MAIL_DEFAULT_SENDER`

The defaults still point at Mandrill / Mailchimp Transactional SMTP, but they are now overrideable through environment variables.

## 4. Use GitHub Codespaces
This repo now includes [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json). Creating a codespace will:

* use Python `3.11`
* install the VS Code Python extensions
* create `.venv`
* sync the checked-in `uv.lock`
* forward port `5000`

After the codespace starts, run:

* `uv run flask db upgrade`
* `uv run python -m unittest discover -s project/tests -v`
* `uv run flask run --host 0.0.0.0 --port 5000`

Store secrets such as `SECRET_KEY` and SMTP credentials in Codespaces repository or organization secrets, not in the repo.

## 5. Deploy to Heroku
As of December 5, 2025, Heroku recommends declaring a Python version in `.python-version`, and as of January 7, 2026 it no longer supports Python 3.9 for new apps. This repo now pins `3.11` to avoid drifting to an untested default runtime.

For a staging app:

1. Create the app:
   `heroku apps:create yourapp-staging`
2. Add a git remote:
   `heroku git:remote -a yourapp-staging --remote staging`
3. Set config vars:
   `heroku config:set APP_SETTINGS=config.StagingConfig SECRET_KEY=change-me -a yourapp-staging`
4. Add PostgreSQL:
   `heroku addons:create heroku-postgresql:essential-0 -a yourapp-staging`
5. Add email config if needed:
   `heroku config:set MAIL_USERNAME=... MAIL_PASSWORD=... MAIL_DEFAULT_SENDER=... -a yourapp-staging`
6. Deploy:
   `git push staging HEAD:master`
7. The release phase in [Procfile](../Procfile) runs `flask db upgrade` automatically during deploy.

Repeat the same flow for production with `config.ProductionConfig`.
