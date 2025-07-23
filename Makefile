build: clean
	yes | pip3 install build twine
	python3 -m build --sdist
	python3 -m build --wheel
	twine check dist/*

.PHONY : build


clean:
	rm -rf dist build

.PHONY : clean


check:
	black src --check --diff
	pylint src --fail-under=10

.PHONY : check


lintfmt:
	black src
	pylint src

.PHONY : lintfmt


test:
	PYTHONPATH=src pytest -q

.PHONY : test
