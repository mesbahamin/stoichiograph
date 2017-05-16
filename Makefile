DATADIR = data/
DATE = `date +%Y-%m-%d`

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf Stoichiograph.egg-info/

init:
	pip install -r dev_requirements.txt

lint:
	flake8 --max-line-length 90 stoichiograph/*.py tests/*.py setup.py

loc:
	cloc --by-file --include-lang=Python .

package: clean lint
	python setup.py sdist bdist_wheel

test:
	# To run individual tests, use "py.test -k the_test_path"
	py.test tests

todo:
	grep -FR --ignore-case --binary-file=without-match todo *.py stoichiograph/ tests/

upload: package
	twine upload dist/*

watch-log:
	tail -f debug.log
