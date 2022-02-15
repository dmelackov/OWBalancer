FROM python:3.7

EXPOSE 80

ENV SITE_PORT="80"
ENV DATABASE_IP="localhost"
ENV DATABASE_PORT="3306"
ENV DATABASE_TABLE="owbalancer"
ENV DATABASE_USER_USERNAME="root"
ENV DATABASE_USER_PASSWORD="root"
ENV DATABASE_TYPE="sqlite"

ENV PYTHONPATH="/usr/src/balancer"

WORKDIR /usr/src/balancer

COPY ./app ./app
COPY ./requirements.txt ./
COPY ./start.py ./
COPY ./logging.conf ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "start.py"]