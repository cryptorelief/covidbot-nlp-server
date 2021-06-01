FROM mavfav/alpandas:latest as builder

WORKDIR /app
RUN apk add --no-cache --update \
        uwsgi-python3

COPY prod.requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r prod.requirements.txt && find /app/.venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+


FROM alpine:3.13
LABEL maintainer="Mayank <mp@mailx.es>"

EXPOSE 4444

WORKDIR /app/http-api
RUN apk add --no-cache --update \
        uwsgi-python3 \
        libstdc++ \
        libpq \
        py-pip

RUN mkdir -p /run/uwsgi/ \
        && pip install uwsgitop \
        && adduser -DHs /sbin/nologin rauser \
        && chown -R rauser.rauser /run/uwsgi/ /app/

COPY --from=builder /app /app/http-api
COPY . /app/http-api
ENV PATH="/app/http-api/.venv/bin:$PATH"
CMD [ "/usr/sbin/uwsgi", "--ini", "/app/http-api/conf/uwsgi.ini" ]
