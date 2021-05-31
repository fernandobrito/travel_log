.PHONY: serve
serve:
	python3 -m http.server -d output/website

.PHONY: build
build:
	python3 src/travel_log/main.py

.PHONY: build-watch
build-watch:
	fswatch --recursive -o src/travel_log/ | xargs -n1 -I{} make build