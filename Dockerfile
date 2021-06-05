FROM mavfav/alpandas:latest as builder

WORKDIR /app
RUN apk add --no-cache --update \
        uwsgi-python3

COPY prod.requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r prod.requirements.txt && find /app/.venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+


FROM alpine:3.13
LABEL maintainer="Mayank <mp@mailx.es>"

EXPOSE 4444

WORKDIR /app/covidbot-nlp-server
RUN apk add --no-cache --update \
        uwsgi-python3 \
        libstdc++ \
        py-pip \
        bash

RUN mkdir -p /run/uwsgi/ \
        && pip install uwsgitop \
        && adduser -DHs /sbin/nologin rauser \
        && chown -R rauser.rauser /run/uwsgi/ /app/

COPY --from=builder /app /app/covidbot-nlp-server
COPY . /app/covidbot-nlp-server
COPY conf/entrypoint.sh /entrypoint.sh
ENV PATH="/app/covidbot-nlp-server/.venv/bin:$PATH"
RUN chown -R rauser.rauser /run/uwsgi/ /app/
USER rauser
CMD [ "/entrypoint.sh" ]
