##@ Lint & Format

.PHONY: lint typecheck format check-all
lint: ## Run ruff linter
	poetry run ruff check zumic

typecheck: ## Run mypy type checks
	poetry run mypy zumic

format: ## Format code using ruff
	poetry run ruff format zumic

check-all: ## Run all checks (lint + typecheck)
	$(MAKE) lint
	$(MAKE) typecheck

##@ Test

.PHONY: test
test: ## Run tests with pytest
	poetry run pytest -v

##@ Clean

.PHONY: clean
clean: ## Remove cache and Python aerifacts
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache dist build

##@ Git

.PHONY: git-add git-commit git-push git-status
git-add: ## Stage all changes
	git add .

git-commit: ## Commit with message. Usage: make git-commit MSG="your message"
ifndef MSG
	$(error MSG is not set. Use make git-commit MSG="your message")
endif
	git commit -m "$(MSG)"

git-push: ## Push to origin
	git push

git-status: ## Git status
	git status

##@ Poetry

.PHONY: install update lock
install: ## Install dependencies
	poetry install

update: ## Update all dependencies
	poetry update

lock: ## Regenerate poetry.lock
	poetry lock

##@ Version & Release

VERSION := v$(shell poetry version -s)

.PHONY: bump-version git-tag release-all
bump-version: ## Bump patch version
	poetry version patch
	git add pyproject.toml
	git commit -m "chore: bump version to $(shell poetry version -s)"

git-tag: ## Create Git tag. Usage: make git-tag VERSION=v0.2.0
ifndef VERSION
	$(error VERSION is not set. Use make git-tag VERSION=v0.2.0)
endif
	git tag $(VERSION)

release-all: ## Full release cycle: bump version + tag + push
	$(MAKE) bump-version
	$(MAKE) git-tag VERSION=$(VERSION)
	git push origin $(VERSION)

##@ Help

.PHONY: help
help: ## Show this help message
	@echo
	@echo "Zumic Python Client Makefile (version $(VERSION))"
	@echo "Usage: make [target]"
	@echo
	@awk 'BEGIN {FS = ":.*##"; \
	  printf "%-20s %s\n", "Target", "Description"; \
	  printf "-------------------  -----------------------------\n"} \
	/^[a-zA-Z0-9_-]+:.*?##/ { printf " \033[36m%-20s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)
