FROM python:3.12.4-slim-bookworm as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root --no-dev

FROM builder-base as development

RUN poetry install --no-root

COPY . .

RUN poetry install

CMD ["python","-m", "myapplication.main"]

FROM python-base as production

COPY --from=builder-base $VENV_PATH $VENV_PATH
WORKDIR $PYSETUP_PATH
COPY ./src/ ./
USER 10000

CMD ["python","-m", "myapplication.main"]
