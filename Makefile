.PHONY: help run-%

help:
	@echo "Available commands:"
	@echo "  make run-Tempus"
	@echo "  make run-Alpha"
	@echo "  make run-Pandora"
	@echo "  make run-Codex"
	@echo "  make run-Equinox"



run-%:
	python -m $*.main
