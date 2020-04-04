FROM python:3.8-slim as development_build

# User ID for the hackathon user being created. The builder can set this
# to the host user's ID to avoid file permissions problems.
# TODO: uncomment user creation when `poetry` add possibility
# to use `pin install --user`.
# ARG USER_ID=1000

ENV PYTHONUNBUFFERED 1
# TODO: uncomment user creation when `poetry` add possibility
# to use `pin install --user`.
# ENV HOME=/home/hackathon
ENV POETRY_VERSION=1.0.5


RUN apt-get -qq update \
    && apt-get -qq -y install \
        curl \
        gcc \
        gettext \
        libpq-dev \
        vim \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# Create the user and group to run the hackathon application as
# TODO: uncomment user creation when `poetry` add possibility
# to use `pin install --user`.
# RUN addgroup \
#         --system \
#         --gid $USER_ID \
#         hackathon \
#     && adduser \
#         --system \
#         --home $HOME \
#         --uid $USER_ID \
#         --ingroup hackathon \
#         hackathon

COPY ./docker/entrypoint_backend.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

COPY ./docker/backend/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh \
    && chmod +x /start.sh

# Prepare Celery worker and flower starting scripts
COPY ./docker/backend/celery/start_worker.sh /start_celeryworker.sh
RUN sed -i 's/\r//' /start_celeryworker.sh \
    && chmod +x /start_celeryworker.sh

COPY ./docker/backend/celery/start_flower.sh /start_celeryflower.sh
RUN sed -i 's/\r//' /start_celeryflower.sh \
    && chmod +x /start_celeryflower.sh


# TODO: uncomment user creation when `poetry` add possibility
# to use `pin install --user`.
# RUN chown -R hackathon /app

# TODO: uncomment user creation when `poetry` add possibility
# to use `pin install --user`.
# USER hackathon
# # add directory with locally installed (via `pip install --user hackathon`)
# # Python modules to `${PATH}`
# # https://docs.python.org/3/library/site.html#site.USER_BASE
# ENV PATH "${PATH}:${PYTHONUSERBASE:-/home/hackathon/.local}/bin"

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
RUN sed -i 's/\r//' /app/pyproject.toml \
    && sed -i'' "s/src\///" /app/pyproject.toml
RUN sed -i 's/\r//' /app/poetry.lock \
    && sed -i'' "s/src\///" /app/poetry.lock

RUN pip install -U pip \
    && pip install "poetry==${POETRY_VERSION}"
# Force `virtualenvs.create false` in case user update it in `pyproject.toml`
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]

 # PRODUCTION ONLY STAGE
FROM development_build as production_build

COPY ./shared/ /app/shared/
COPY ./backend /app
