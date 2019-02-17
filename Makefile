ENV := DEV
postgres_version = 11.1
postgres_password = $(shell ENV=$(ENV) pipenv run python config.py database password)
postgres_url = $(shell ENV=$(ENV) pipenv run python config.py database url)
dbmate_version = v1.4.1

install:
	pipenv install

test:
	export ENV=$(ENV)
	make run-test-db
	pipenv run pytest -v
	make stop-test-db

run-test-db:
	docker run --name tweet-postgres-tests -e POSTGRES_PASSWORD=$(postgres_password) --rm -p 5432:5432 -d postgres:$(postgres_version)
	make migration cmd=wait
	make migration cmd=migrate

stop-test-db:
	docker stop tweet-postgres-tests

migration:
	docker run \
	--net=host -v `pwd`/db:/db -w / \
	-e "DATABASE_URL=$(postgres_url)?sslmode=disable" \
	--rm amacneil/dbmate:$(dbmate_version) $(cmd)
