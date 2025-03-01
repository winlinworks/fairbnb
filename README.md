# Fairbnb
Welcome to Fairbnb, a clone of Airbnb. This doc aims to quickly onboard devs to the product, including local dev setup, tools, patterns, and ways of working. To suggest edits, open an issue in this repo.

## Set up local back-end dev environment
To load virtual environment in your shell, go to the `backend` folder and run `poetry shell`. Dependencies for the app are included in the `poetry.lock` and `pyproject.toml` files. To update and install dependencies, use `poetry add` followed by `poetry install`; avoid editing `pyproject.toml` directly (but run `poetry update` if you do). You can also load the virtual environment separately for each command by running `poetry run {your command}`.

Create a file `backend/.env.docker` with the environment variables below for the BE container. You can also run `source .env.docker` to add the environment variables to your local machine for development before building the BE container.
```
# Dev database credentials
export POSTGRES_USER="{username}"
export POSTGRES_PASS="{password}"
export POSTGRES_HOST="{db-host}"
export POSTGRES_PORT="{db-port}"
export POSTGRES_DB="{db-name}"

# Django environment variables to develop on local machine (not container)
export DJANGO_SETTINGS_MODULE="src.db.settings"
export DJANGO_SECRET_KEY="{django-secret-key}"
```

## Set up local front-end dev environment
Create a file `frontend/.env` with the environment variables below for the FE container.
```
export NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY={clerk-key}
export CLERK_SECRET_KEY={clerk-secret}

export NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/profile/create
export NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/profile/create
export NEXT_PUBLIC_API_URL=127.0.0.1:8000
```

## Run app locally
Make sure to complete the above setup for local BE and FE dev environments before building the containers. To run the application for development, go to the project root folder and run `docker compose up --build -d`. You can also use Podman, a more secure and container/pod manager, by running `podman compose up --build -d`. View the website by visiting `http://127.0.0.1:3000` in a browser.

After running the app locally, you can view the API docs by visiting `http://127.0.0.1:8000/docs` in a browser.

## Contribute to the project
To manage contributions, we use 4 types of issues below. The title should include the bolded prefix along with a short description to make it easier to understand (e.g., feat: Add user auth, fix: Server error for GET review).
1. **feat:** Suggest a new feature or change to an existing one
2. **fix:** Report a bug that needs to be fixed
3. **chore:** Suggest a chore, such as updating documentation or refactoring code
4. **spike:** Research designs, methods, or tools

To be ready for work, an issue must have the following info:
- Priority: P0 - Critical, P1 - High, P2 - Moderate, P3 - Low, or P4 - Negligible
- Estimate: 1, 2, 3, 5, 8, 13
- Iteration
- Assignees
- Projects: Fairbnb

Assignees and labels can be added to issues as appropriate:
- Acceptance Criteria (in description)
- Labels

## Coding standards
To ensure high quality code, we follow these standards:
- [Google style Python docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

## Knowledge base
To access tools for communication, planning, design, and project management, visit our [Knowledge Base](https://winlin.atlassian.net/wiki/spaces/Fairbnb/overview?homepageId=246579754).
