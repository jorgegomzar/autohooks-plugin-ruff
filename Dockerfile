FROM python:3.7

ARG GIT_EMAIL=""
ARG GIT_NAME=""
RUN git config --global user.email "${GIT_EMAIL}"
RUN git config --global user.name "${GIT_NAME}"

RUN mkdir -p /src
WORKDIR /src

RUN pip install "poetry>=1.5.1,<1.6"

COPY poetry.lock /src/poetry.lock
COPY pyproject.toml /src/pyproject.toml
COPY autohooks /src/autohooks
COPY README.md /src/README.md

RUN poetry config virtualenvs.create false
RUN poetry install --with dev,test

ENV PYTHONPATH .
# Docker dev env
CMD ["tail", "-f", "/dev/null"]