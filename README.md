# Hack Yeah 2020

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Backend

### Docker

`docker-compose` is required to run backend server in container.

Before building images populate environment variable file:

Edit files located in `.envs/` directory according to your needs.

Build docker images:

```bash
docker-compose build
```

To run all services (API, Celery and Databases):

```bash
docker-compose up
```

To run tests use `pytest` command e.g.:

```bash
docker-compose run --rm app pytest
```

To lint code use `flake8` command e.g.:

```bash
docker-compose run --rm app flake8
```
