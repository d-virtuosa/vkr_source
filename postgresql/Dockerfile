FROM postgres:15.0-alpine
ENV POSTGRES_PASSWORD q1w2e3r4t5
ENV POSTGRES_DB blog
COPY init.sql /docker-entrypoint-initdb.d/
COPY secret_db.txt /
