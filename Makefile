install: requirements.txt
	python -m pip install --upgrade pip
	pip install -r requirements.txt


# Alpha execution commands--

test-Alpha:
	python -m pytest -v Alpha/tests/

run-Alpha:
	python -m Alpha.main

