code-convention:
	flake8

run:
	flask run

test:
	coverage run -m pytest
	coverage report

init-db:
	flask db init

upgrade-db:
	flask db upgrade

