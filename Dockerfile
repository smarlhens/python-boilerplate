FROM python:3.12.7-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORKDIR_PATH="/opt/python-boilerplate" \
    VIRTUAL_ENV="/opt/python-boilerplate/.venv"

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM python-base AS builder-base

COPY --from=ghcr.io/astral-sh/uv:0.4.27 /uv /bin/uv

WORKDIR $WORKDIR_PATH

COPY . .

RUN uv sync --frozen

FROM builder-base AS development

CMD ["python","-m", "python_boilerplate.main"]

FROM python-base AS production

COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR $WORKDIR_PATH

COPY ./src/ ./

USER 10000

CMD ["python","-m", "python_boilerplate.main"]
