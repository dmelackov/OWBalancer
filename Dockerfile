FROM python:3.7

EXPOSE 8080

ENV SITE_PORT="8080"
ENV PYTHONPATH="/usr/src/balancer"

WORKDIR /usr/src/balancer

COPY ./app ./
COPY ./requirements.txt ./
COPY ./start.py ./
COPY ./logging.conf ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "start.py"]