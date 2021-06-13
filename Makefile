.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	mypy src/
	black .
	flake8

.PHONY: serve
serve:
	python3 -m http.server -d output/website

.PHONY: build
build:
	python3 src/travel_log/main.py --input-folder=./test/_sample_project

.PHONY: build-watch
build-watch:
	fswatch --recursive -o src/travel_log/ | xargs -n1 -I{} make build

.PHONY: deploy-netlify-draft
deploy-netlify-draft:
	netlify deploy --dir=output/website

.PHONY: deploy-netlify-prod
deploy-netlify-prod:
	netlify deploy --dir=output/website --prod

