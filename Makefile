MAIN = src/app.py

.PHONY: dev

dev:
	uv run $(MAIN)