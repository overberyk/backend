FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /code
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY pyproject.toml uv.lock* /code/
RUN uv sync --no-install-project
COPY . /code/
RUN uv sync
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "App:app", "--host", "0.0.0.0", "--port", "8000"]
