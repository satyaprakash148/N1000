load:
	python src/etl/loader.py

validate:
	python src/etl/validator.py

test:
	pytest tests/etl/

clean:
	rm -rf output/*