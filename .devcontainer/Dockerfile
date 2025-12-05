FROM ghcr.io/astral-sh/uv:python3.10-alpine

RUN groupadd --gid 2000 dev && \
    useradd --uid 2000 --gid 2000 -m dev

USER dev
