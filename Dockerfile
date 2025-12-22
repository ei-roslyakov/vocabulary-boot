FROM python:3.14.2-slim-bookworm

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

RUN chown -R appuser:appuser /usr/app

USER appuser

WORKDIR /usr/app

CMD [ "python", "-m", "bot" ]
