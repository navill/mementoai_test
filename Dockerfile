FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    default-mysql-server \
    redis \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY docker_files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker_files/redis.conf /etc/redis/redis.conf
RUN pip install --no-cache-dir -r requirements.txt

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME

ENV DB_USERNAME=$DB_USERNAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_NAME=$DB_NAME
ENV CELERY_BROKER=redis://localhost:6379/0

COPY . .

EXPOSE 8000

RUN service mariadb start \
  && mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME; \
  CREATE USER IF NOT EXISTS '$DB_USERNAME'@'$DB_HOST' IDENTIFIED BY '$DB_PASSWORD'; \
  GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USERNAME'@'$DB_HOST';"

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
