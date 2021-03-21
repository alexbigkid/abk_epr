.PHONY:	init init_dev test settings help

init:
	pip3 install --upgrade setuptools
	pip3 install --user -r requirements.txt

init_dev:	init
	pip3 install --user -r requirements_dev.txt

test:
	py.test tests

settings:
	@echo "HOME             =" ${HOME}
	@echo "SHELL            =" ${SHELL}

help:
	@echo "Targets:"
	@echo "  init           - installs required packages"
	@echo "  init_dev       - installs required development packages"
	@echo "  test           - runs pytest"
	@echo "  settings       - outputs current settings"
	@echo "  help           - outputs this info"
