clean:
	-rm data/*.csv

test: clean
	pytest

export-env:
	conda env export > environment.yml
