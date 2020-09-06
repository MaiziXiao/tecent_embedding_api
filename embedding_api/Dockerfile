FROM google/cloud-sdk:latest

RUN apt-get update \
    && apt-get -y install python3 python3-dev python3-venv \
    && pip3 install poetry

COPY poetry.lock pyproject.toml /

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
