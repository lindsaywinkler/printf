
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

# Pre-compile Python to .pyc
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev


# Two stage build for smaller image.  Don't need uv in the final 
# image, for example.
#
# So we start again from a base layer and just copy across
# all the files that uv installed for us in the previous
# step.
FROM python:3.14-slim

WORKDIR /app

RUN useradd --system --no-create-home app

COPY --from=builder /app/.venv /app/.venv
COPY . .

USER app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]
