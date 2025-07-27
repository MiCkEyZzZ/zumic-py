lint:
	poetry run ruff check zumic

typecheck:
	poetry run mypy zumic

test:
	poetry run pytest -v
