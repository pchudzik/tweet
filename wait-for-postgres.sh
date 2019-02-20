#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
user="$2"
password="$3"
version="$4"

until docker run --link "$host" --rm -e PGPASSWORD="$password" postgres:"$version" psql -h "$host" -U "$user" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 0.2
done

>&2 echo "Postgres is up!"
