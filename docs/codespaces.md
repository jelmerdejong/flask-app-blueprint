# GitHub Codespaces
This repository includes a checked-in devcontainer at [`.devcontainer/devcontainer.json`](../.devcontainer/devcontainer.json).

## What the devcontainer does
* uses Python `3.11`
* creates `.venv` inside the workspace
* syncs the checked-in `uv.lock`
* forwards port `5000`
* configures the VS Code Python extensions

## First run
After the codespace finishes creating, run:

1. `uv run flask db upgrade`
2. `uv run python -m unittest discover -s project/tests -v`
3. `uv run flask run --host 0.0.0.0 --port 5000`

Open the forwarded port for the running Flask app when prompted by Codespaces.

## Secrets and configuration
Keep secrets out of the repository. For Codespaces, set values such as these through Codespaces secrets:

* `SECRET_KEY`
* `DATABASE_URL` if you want PostgreSQL instead of SQLite
* `MAIL_USERNAME`
* `MAIL_PASSWORD`
* `MAIL_DEFAULT_SENDER`

You can also keep non-secret local overrides in `.env`, which is now ignored by git.
