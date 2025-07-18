install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

dev:
	. .venv/bin/activate && python run.py

run:
	. .venv/bin/activate && python run.py

freeze:
	pip freeze > requirements.txt
