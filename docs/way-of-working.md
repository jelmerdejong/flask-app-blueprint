# Way of Working
Few points to keep in mind when you extend this blueprint:

1. Run the test suite before you push:
   `uv run python -m unittest discover -s project/tests -v`
2. Keep secrets in `.env`, Codespaces secrets, or Heroku config vars. Do not commit them.
3. Prefer staging-first deployment if you keep separate Heroku apps.
4. Keep dependency updates intentional. This repo now uses `pyproject.toml` plus `uv.lock`.

## Updating dependencies
1. Add or update dependencies with `uv add`, `uv remove`, or `uv lock --upgrade-package`
2. Verify the app boots, migrations run, and tests pass
3. Commit both `pyproject.toml` and `uv.lock`

## Database workflow
1. Generate or edit migrations when models change
2. Apply them locally with `uv run flask db upgrade`
3. Heroku deployments run migrations automatically through the `release` process in `Procfile`
