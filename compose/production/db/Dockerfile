FROM postgres

RUN echo "CREATE DATABASE {DB_NAME};\
     CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';\
     ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';\
     ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';\
     ALTER ROLE {DB_USER} SET timezone TO 'UTC';" | psql

