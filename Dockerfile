FROM python:3.7-slim

EXPOSE 80

ENV SITE_PORT="80" \
    DATABASE_IP="localhost" \
    DATABASE_PORT="3306" \
    DATABASE_TABLE="owbalancer" \
    DATABASE_USER_USERNAME="root" \
    DATABASE_USER_PASSWORD="root" \
    DATABASE_TYPE="sqlite"

ENV PYTHONPATH="/usr/src/balancer"

WORKDIR /usr/src/balancer

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD [ "python3", "start.py"]