.PHONY: help run-%

help:
	@echo "Available commands:"
	@echo "  make run-Tempus"
	@echo "  make run-Alpha"
	@echo "  make run-Pandora"
	@echo "  make run-Codex"



run-%:
	python -m $*.main
