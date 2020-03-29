code-convention:
	flake8

run:
	flask init-db
	flask run

test:
	coverage run -m pytest
	coverage report
