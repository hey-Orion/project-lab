.PHONY: install test run

install: requirements.txt
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt

# execution commands--

test:
	python3 -m pytest -v tests/

run:
	python3 -m src.pipeline_runner