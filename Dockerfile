FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update
RUN apt upgrade -y
RUN apt install build-essential -y
RUN python -m pip install --upgrade pip

# Have to install some libraries in order for fbprophet to install correctly
RUN python -m pip install pystan==3.0.0b5 pandas==1.2.0rc0
RUN python -m pip install fbprophet==0.7.1

# Install the rest of the requirements
RUN python -m pip install -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]
