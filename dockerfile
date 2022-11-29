# syntax=docker/dockerfile:1

FROM python:3.10

RUN apt-get update && apt-get install -y supervisor && apt-get install -y redis
RUN mkdir -p /var/log/supervisor
RUN cat > /var/log/supervisor/supervisor.log

WORKDIR /app
RUN mkdir /cloud


COPY ./requirements.txt .
RUN pip3 install -U pip wheel cmake
RUN pip3 install --upgrade pip \
        && apt-get install -y --fix-missing\
        && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/usr/bin/supervisord", "-c", "./supervisord.conf"]
