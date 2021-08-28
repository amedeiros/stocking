FROM python:3.7

WORKDIR /usr/src/app

ENV PYTHONPATH /usr/src/app

RUN apt update
RUN apt upgrade -y
RUN apt install build-essential -y
RUN python -m pip install --upgrade pip

COPY . .

# Build requirements for facebook prophet
RUN python -m pip install pystan==2.19.1.1 numpy==1.21.2
# Install the rest of the requirements
RUN python -m pip install -r requirements.txt -r requirements-dev.txt
