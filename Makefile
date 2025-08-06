test:
	poetry run pytest --ignore tests/test_focus_data_upload.py
test-full:
	poetry run pytest
build:
	poetry build