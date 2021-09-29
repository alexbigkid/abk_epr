.PHONY:	upgrade_setuptools install install_dev test test_verbose exif_rename exif_rename3 settings help
.SILENT: exif_rename exif_rename3 coverage

# python is sometimes linked to python v2 and sometimes to python v3
# So to make sure make rules work on other computers 2nd set of rules are created
upgrade_setuptools:
	pip install --upgrade setuptools

install: upgrade_setuptools
	pip install --user --requirement requirements.txt

install_dev: upgrade_setuptools
	pip install --user --requirement requirements_dev.txt

test:
	python -m unittest discover --start-directory tests

test_verbose:
	python -m unittest discover --start-directory tests --verbose

exif_rename:
	python ./src/main.py

# ----------------------------
# if python3 is defined
# ----------------------------
upgrade_setuptools3:
	pip3 install --upgrade setuptools

install3: upgrade_setuptools3
	pip3 install --user --requirement requirements.txt

install_dev3: upgrade_setuptools3
	pip3 install --user --requirement requirements_dev.txt

test3:
	python3 -m unittest discover --start-directory tests

test_verbose3:
	python3 -m unittest discover --start-directory tests --verbose

exif_rename3:
	python3 ./src/main.py

# ----------------------------
# those rules should be universal
# ----------------------------
coverage:
	coverage run --source src --omit src/__init__.py -m unittest discover --start-directory tests
	@echo
	coverage report
	coverage xml

settings:
	@echo "HOME             = ${HOME}"
	@echo "PWD              = ${PWD}"
	@echo "SHELL            = ${SHELL}"

help:
	@echo "Targets:"
	@echo "-----------------------------------------------------------------------------"
	@echo "  exif_rename  - executes the main program"
	@echo "  install      - installs required packages"
	@echo "  install_dev  - installs required development packages"
	@echo "  test         - runs test"
	@echo "  test_verbose - runs test with verbose messaging"
	@echo "-----------------------------------------------------------------------------"
	@echo "  exif_rename3 - executes the main program with python3"
	@echo "  install3     - installs required packages with python3"
	@echo "  install_dev3 - installs required development packages with python3"
	@echo "  test3        - runs test with python3"
	@echo "  test_verbose3- runs test with verbose messaging with python3"
	@echo "-----------------------------------------------------------------------------"
	@echo "  coverage     - runs test, produces coverage and displays it"
	@echo "  settings     - outputs current settings"
	@echo "  help         - outputs this info"
