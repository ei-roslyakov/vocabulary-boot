FROM python:3.9.2-slim-buster

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

WORKDIR /usr/app

CMD [ "python", "-m", "bot" ]
