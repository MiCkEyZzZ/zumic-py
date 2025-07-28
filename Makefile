##@ Lint & Format

.PHONY: lint typecheck format check-all
lint: ## Запустить линтер ruff
	poetry run ruff check zumic

typecheck: ## Запустить проверку типов с помощью mypy
	poetry run mypy zumic

format: ## Отформатировать код с помощью ruff
	poetry run ruff format zumic

check-all: ## Запустить все проверки (линтер + проверка типов)
	$(MAKE) lint
	$(MAKE) typecheck

##@ Test

.PHONY: test
test: ## Запустить тесты с помощью pytest
	poetry run pytest -v

##@ Clean

.PHONY: clean
clean: ## Удалить кэш и артефакты Python
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache dist build

##@ Git

.PHONY: git-add git-commit git-push git-status
git-add: ## Добавить все изменения в индекс
	git add .

git-commit: ## Сделать коммит с сообщением. Использование: make git-commit MSG="ваше сообщение"
ifndef MSG
	$(error MSG is not set. Use make git-commit MSG="your message")
endif
	git commit -m "$(MSG)"

git-push: ## Отправить изменения в origin
	git push

git-status: ## Показать статус Git
	git status

##@ Poetry

.PHONY: install update lock
install: ## Установить зависимости
	poetry install

update: ## Обновить все зависимости
	poetry update

lock: ## Перегенерировать файл poetry.lock
	poetry lock

##@ Version & Release

VERSION := v$(shell poetry version -s)

.PHONY: bump-version git-tag release-all
bump-version: ## Увеличить версию патча
	poetry version patch
	git add pyproject.toml
	git commit -m "chore: bump version to $(shell poetry version -s)"

git-tag: ## Создать Git-тег. Использование: make git-tag VERSION=v0.2.0
ifndef VERSION
	$(error VERSION is not set. Use make git-tag VERSION=v0.2.0)
endif
	git tag $(VERSION)

release-all: ## Полный цикл релиза: bump версии, создание тега, пуш
	$(MAKE) bump-version
	$(MAKE) git-tag VERSION=$(VERSION)
	git push origin $(VERSION)

##@ Help

.PHONY: help
help: ## Показать это справочное сообщение
	@echo
	@echo "Zumic Python Client Makefile (версия $(VERSION))"
	@echo "Использование: make [цель]"
	@echo
	@awk 'BEGIN {FS = ":.*##"; \
	  printf "%-20s %s\n", "Цель", " Описание"; \
	  printf "--------------------  -----------------------------\n"} \
	/^[a-zA-Z0-9_-]+:.*?##/ { printf " \033[36m%-20s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)
