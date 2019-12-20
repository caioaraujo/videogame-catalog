# videogame-catalog
A Flask experiment.

## Requirements

- Python 3.8

Optional:
- Pipenv
- GNU Make

## Installation

You can install all dependencies and creating a virtualenv with pipenv (https://pipenv.readthedocs.io/en/latest/install/),
by running:

`pipenv install`

Make a local copy of `local.env` file as `.env`. Once this project uses python-dotenv lib, all environment variables in .env value will be used in local running.

## Running 

### Local

`flask init-db && flask run`<br>
or<br>
`make run`

### Coding style tests

This project uses flake8 checking. Install all development dependencies and execute:

`flake8`

or

`make code-convention`
