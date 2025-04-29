FROM python:3.11-buster AS builder

RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster AS runtime

WORKDIR /code

ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY query ./query

CMD ["python", "query/main.py"]