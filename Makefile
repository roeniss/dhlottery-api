build: clean
	yes | pip3 install build twine
	python3 -m build --sdist
	python3 -m build --wheel
	twine check dist/*

.PHONY : build


clean:
	rm -rf dist build

.PHONY : clean


lintfmt:
	black src/**
	pylint src

.PHONY : lintfmt


test:
	PYTHONPATH=src pytest -q

.PHONY : test
