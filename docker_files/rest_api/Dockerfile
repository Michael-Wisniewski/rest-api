FROM alpine:3.8

LABEL maintainer="Michał Wiśniewski <mikex929@gmail.com>"
LABEL description="Python RESTful Application"

RUN mkdir -p /rest_api/src && \
    mkdir /rest_api/static
WORKDIR /rest_api
COPY ./config ./

RUN apk update && \
    apk upgrade
RUN apk add --update --no-cache \
        python3 \
        python3-dev \
        build-base \
        linux-headers \
        pcre-dev \
        postgresql-dev \
        musl-dev

RUN pip3 install --no-cache-dir -r requirements.txt

RUN addgroup -g 1000 -S uwsgi_group && \
    adduser -D -H -u 1000 -S uwsgi_admin -G uwsgi_group

USER uwsgi_admin

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]