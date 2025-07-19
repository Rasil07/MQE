# Makefile
# This Makefile is used to install the dependencies and run the application
# It is used to simplify the process of setting up and running the application
# It is used to simplify the process of setting up and running the application


install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

dev:
	. .venv/bin/activate && python run.py

run:
	. .venv/bin/activate && python run.py

freeze:
	pip freeze > requirements.txt
