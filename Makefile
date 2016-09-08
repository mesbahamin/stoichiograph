DATADIR = data/
DATE = `date +%Y-%m-%d`

init:
	pip install -r dev_requirements.txt

test:
	# To run individual tests, use "py.test -k the_test_path"
	py.test tests.py

lint:
	flake8 *.py

watch-log:
	tail -f debug.log

loc:
	cloc --by-file --include-lang=Python .

todo:
	grep -FR --ignore-case --binary-file=without-match todo *.py
