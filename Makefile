.PHONY: build check test test-python test-node clean

build:
	python scripts/build.py

check:
	python scripts/build.py --check

test-python:
	cd packages/python && pytest -v

test-node:
	cd packages/node && npm run build && npm test

test: build test-python test-node

clean:
	rm -rf dist packages/node/dist packages/node/src/data.ts packages/python/src/algeria_geo/data
