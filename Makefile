.PHONY: build check test clean

build:
	python scripts/build.py

check:
	python scripts/build.py --check

test: build
	cd packages/python && pip install -e . pytest && pytest -q
	cd packages/node && npm install && npm run build && npm test

clean:
	rm -rf dist packages/node/dist packages/node/src/data.ts packages/python/src/algeria_geo/data
