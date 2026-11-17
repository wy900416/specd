.PHONY: check validate fitness scan test build stats clean

check: validate fitness scan test

validate:
	python3 -m specd validate

fitness:
	python3 -m specd fitness

scan:
	python3 -m specd scan

test:
	python3 -m unittest discover -s tests -v

build:
	python3 -m specd build

stats:
	python3 -m specd stats

clean:
	rm -rf dist index.json .specd __pycache__ specd/__pycache__ tests/__pycache__
