.PHONY: install up down

install:
	python3 -m pip install --upgrade pip
	pip3 install pytest apache-airflow

up:
	docker compose up --build -d

down:
	docker compose down -v

