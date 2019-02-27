ENV := DEV
postgres_version = 11.1
postgres_password = $(shell ENV=$(ENV) pipenv run python config.py database password)
database_host = $(shell ENV=$(ENV) pipenv run python config.py database host)
database_port = $(shell ENV=$(ENV) pipenv run python config.py database port)
dbmate_version = v1.4.1

install:
	pipenv install

run:
	make run-test-db
	pipenv run python api.py && make stop-test-db

test:
	export ENV=$(ENV)
	make run-test-db
	pipenv run pytest -v -W ignore::DeprecationWarning -W ignore::UserWarning
	make stop-test-db

run-test-db:
	docker run --name tweet-postgres-tests -e POSTGRES_PASSWORD=$(postgres_password) --rm -p 5432:5432 -d postgres:$(postgres_version)
	./wait-for-postgres.sh tweet-postgres-tests postgres $(postgres_password) $(postgres_version)
	pipenv run alembic upgrade head

stop-test-db:
	docker stop tweet-postgres-tests

