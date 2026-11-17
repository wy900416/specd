.PHONY: check validate index fitness scan build context stats

check: validate fitness scan

validate:
	./specd.sh validate

index:
	./specd.sh index

fitness:
	./specd.sh fitness

scan:
	./specd.sh scan --strict

build:
	./specd.sh build

context:
	./specd.sh context orders --task "add idempotency to order creation" --budget 8000

stats:
	./specd.sh stats
