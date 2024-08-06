FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONPATH /usr/src/app

RUN apt update && \
  apt upgrade -y && \
  apt install build-essential -y

RUN python -m pip install --upgrade pip

COPY . .

# Build requirements for facebook prophet
RUN pip install pipenv && \
  pipenv install --system --deploy --ignore-pipfile && \
  pipenv clean
