#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
user="$2"
password="$3"
version="$4"

echo -n "Postgres is unavailable - sleeping"
until docker exec -e PGPASSWORD="$password" "$host" psql -h "localhost" -U "$user" -c '\q' > /dev/null 2>&1; do
  echo -n "."
  sleep 0.2
done

echo "Postgres is up!"
