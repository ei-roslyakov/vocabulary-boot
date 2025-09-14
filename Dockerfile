FROM python:3.14.0rc2-slim-bookworm

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

WORKDIR /usr/app

CMD [ "python", "-m", "bot" ]
