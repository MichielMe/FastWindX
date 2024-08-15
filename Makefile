create_venv:
	/bin/bash ./run.sh create_venv

activate_venv:
	/bin/bash ./run.sh activate_venv

install:
	/bin/bash ./run.sh install

update_hooks:
	/bin/bash ./run.sh update_hooks

lint:
	/bin/bash ./run.sh lint

before_build: create_venv install update_hooks lint

build:
	/bin/bash ./run.sh build

publish_test:
	/bin/bash ./run.sh publish:test

release_test:
	/bin/bash ./run.sh release:test

clean:
	/bin/bash ./run.sh clean
