FROM python:3.11

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./app/uv.lock,target=uv.lock \
    --mount=type=bind,source=./app/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project



ADD ./app /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]