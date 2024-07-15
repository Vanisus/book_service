#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER user WITH PASSWORD 'password';
    CREATE DATABASE book_service;
    GRANT ALL PRIVILEGES ON DATABASE book_service TO user;
EOSQL
