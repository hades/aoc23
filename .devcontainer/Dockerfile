FROM python:3.10

RUN groupadd --gid 2000 dev && \
    useradd --uid 2000 --gid 2000 -m dev && \
    pip install poetry

USER dev
