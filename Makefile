.PHONY: help run-%

help:
	@echo "Available commands:"
	@echo "  make run-Alpha"
	@echo "  make run-Bravo"
	@echo "  make run-Charlie"
	@echo "  make run-Delta"
	@echo "  make run-Echo"
	@echo "  make run-Tempus"



run-%:
	python -m $*.main
