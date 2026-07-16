.PHONY: install run test format lint sast vuln secrets all

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	python -m pytest

format:
	black .

lint:
	flake8 app tests

sast:
	bandit -r app

vuln:
	-pip-audit

secrets:
	detect-secrets scan

all:
	python -m pytest
	bandit -r app
	pip-audit
	detect-secrets scan