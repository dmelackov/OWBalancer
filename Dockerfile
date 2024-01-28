FROM python:3.12-slim

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

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "start.py"]