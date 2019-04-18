FROM node:8

LABEL maintainer="Michał Wiśniewski <mikex929@gmail.com>"
LABEL description="Vue RESTful Application"

WORKDIR /usr/src/app/

COPY ./src/vue_api/package*.json ./

RUN npm install

EXPOSE 8080
CMD [ "npm", "start" ]