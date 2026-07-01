.PHONY: install test run

install: requirements.txt
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# execution commands--

test:
	python -m pytest -v tests/

run:
	python -m src.main