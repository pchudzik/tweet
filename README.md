# tweet

Something like a tweeter clone to bootstrap learning process of database and REST tools in python

## Testing

### `make test`

Will start unit tests. 

### Local development

To run tests on local machine running postgres instance is required to quickly start it you can execute `make
run-test-db` and stop it using `stop-test-db`

### Database migrations

During testing migration are executed as a part of the process (only during `make test` or when starting db `make
run-test-db`). If you want to trigger migrations you can run `make migration cmd="up"` which will migrate db to latest
version. Migrations are managed by tool called dbmate. You can pass any command to docker image by specifying `cmd`
param eg: `make migration cmd="help"` will print all commands ale help.
