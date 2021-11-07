ABSOLUTE_PATH := $(shell pwd)

############ COMMON COMMANDS ############
.PHONY: lint
lint:
	black --check --diff --line-length 120 .

.PHONY: sort
sort:
	isort .

.PHONY: fmt
fmt: sort
	black --line-length 120 .

.PHONY: vet
vet:
	mypy .

.PHONY: uml
uml:
	@plantuml -tsvg ./plantuml -o svg
	@plantuml -tpng ./plantuml -o png

.PHONY: install_prettier
install_prettier:
	npm install

.PHONY: format_md
format_md: install_prettier
	npx prettier --write .

.PHONY: req
req:
	poetry export \
		--without-hashes \
		-f requirements.txt \
		--output requirements.txt

.PHONY: install_dep
install_dep:
	pip install -r requirements.txt
