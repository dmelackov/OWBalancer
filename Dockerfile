FROM yicktop/nginx-node:latest

WORKDIR /usr/share/node/html


COPY ./src /usr/share/node/html/src
COPY ./public /usr/share/node/html/public
COPY ./babel.config.js /usr/share/node/html
COPY ./vue.config.js /usr/share/node/html
COPY ./package.json /usr/share/node/html

RUN npm install && \
    npm run build
RUN cp -R /usr/share/node/html/dist /usr/share/nginx/html
RUN apt-get -qy autoremove
RUN rm -R /usr/share/node/html

WORKDIR /usr/share/nginx/html

COPY ./nginx/ /etc/nginx/

VOLUME /usr/share/nginx/html
VOLUME /etc/nginx