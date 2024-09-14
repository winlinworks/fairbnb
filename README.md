# fairbnb
Welcome to Fairbnb, a clone of Airbnb.

## Set up local dev environment
To load virtual environment in your shell, run `poetry shell`. Dependencies for the app are included in the `poetry.lock` and `pyproject.toml` files. You can also load the virtual environment separately for each command by running `poetry run {your command}`.

## Run app locally
To run the application for development, run `docker compose up --build --watch -d`.

After running the app locally, you can view the API docs by visiting `http://127.0.0.1:8000/docs` in a browser.


## Coding standards
- [Google style Python docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
