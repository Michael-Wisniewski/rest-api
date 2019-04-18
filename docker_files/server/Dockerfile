FROM nginx:1.15.6-alpine

LABEL maintainer="Michał Wiśniewski <mikex929@gmail.com>"
LABEL description="RESTful Application Server"

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /rest_api/static
RUN mkdir /vue_api 

WORKDIR /rest_api
COPY ./config/rest_api_nginx.conf /etc/nginx/conf.d/

EXPOSE 80
EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]