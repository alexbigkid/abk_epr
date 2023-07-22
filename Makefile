.PHONY:	upgrade_setuptools install install_dev install_nth test test_v test_ff test_vff settings help
.SILENT: epr coverage clean
EPR_HOME = src

# -----------------------------------------------------------------------------
# abk_epr Makefile rules
# -----------------------------------------------------------------------------
epr:
	echo "[ python ./src/abk_epr.py -d ./data/20110709_canon -c ./src/logging.yaml -v ]"
	echo "------------------------------------------------------------------------------------"
	cd $(EPR_HOME) && python abk_epr.py -d ../data/20110709_canon -c logging.yaml -v

epr_log:
	cd $(EPR_HOME) && python abk_epr.py -d ../data/20110709_canon -c logging.yaml -l -v

epr_trace:
	cd $(EPR_HOME) && python abk_epr.py -d ../data/20110709_canon -c logging.yaml -v


# -----------------------------------------------------------------------------
# Dependency installation Makefile rules
# -----------------------------------------------------------------------------
upgrade_setuptools:
	pip install --upgrade setuptools

install: upgrade_setuptools
	pip install --requirement requirements.txt

install_test: upgrade_setuptools
	pip install --requirement requirements_test.txt

install_dev: upgrade_setuptools
	pip install --requirement requirements_dev.txt


# -----------------------------------------------------------------------------
# Running tests Makefile rules
# -----------------------------------------------------------------------------
test:
	python -m unittest discover --start-directory tests

test_ff:
	python -m unittest discover --start-directory tests --failfast

test_v:
	python -m unittest discover --start-directory tests --verbose

test_vff:
	python -m unittest discover --start-directory tests --verbose --failfast

%:
	@:

test_1:
	python -m unittest "tests.$(filter-out $@,$(MAKECMDGOALS))"

coverage:
	coverage run --source $(EPR_HOME) --omit ./tests/*,./$(EPR_HOME)/config/*  -m unittest discover --start-directory tests
	@echo
	coverage report
	coverage xml

# coverage:
# 	coverage run --source src --omit src/__init__.py -m unittest discover --start-directory tests
# 	@echo
# 	coverage report
# 	coverage xml


# -----------------------------------------------------------------------------
# Package bulding and deploying Makefile rules
# -----------------------------------------------------------------------------
sdist: upgrade_setuptools
	@echo "[ python setup.py sdist ]"
	@echo "------------------------------------------------------------------------------------"
	python setup.py sdist

build: upgrade_setuptools
	@echo "[ python -m build ]"
	@echo "------------------------------------------------------------------------------------"
	python -m build

wheel: upgrade_setuptools
	@echo "[ python -m build ]"
	@echo "------------------------------------------------------------------------------------"
	python -m build --wheel

testpypi: wheel
	@echo "[ twine upload -r testpypi dist/*]"
	@echo "------------------------------------------------------------------------------------"
	twine upload -r testpypi dist/*

pypi: wheel
	@echo "[ twine upload -r pypi dist/* ]"
	@echo "------------------------------------------------------------------------------------"
	twine upload -r pypi dist/*


# -----------------------------------------------------------------------------
# Clean up Makefile rules
# -----------------------------------------------------------------------------
clean:
	@echo "deleting log files:"
	@echo "___________________"
	@if [ -f logs/* ]; then ls -la logs/*; fi;
	@if [ -f logs/* ]; then rm -rf logs/*; fi;
	@echo
	@echo "deleting dist files:"
	@echo "___________________"
	@if [ -d dist ]; then ls -la dist; fi;
	@if [ -d dist ]; then rm -rf dist; fi;
	@echo
	@echo "deleting build files:"
	@echo "___________________"
	@if [ -d build ]; then ls -la build; fi;
	@if [ -d build ]; then rm -rf build; fi;
	@echo
	@echo "deleting egg-info files:"
	@echo "___________________"
	@if [ -d *.egg-info ]; then ls -la *.egg-info; fi
	@if [ -d *.egg-info ]; then rm -rf *.egg-info; fi
	@echo
	@echo "deleting __pycache__ directories:"
	@echo "___________________"
	find . -name "__pycache__" -type d -prune
	rm -rf  $(find . -name "__pycache__" -type d -prune)


# ----------------------------
# those rules should be universal
# ----------------------------
settings:
	@echo "HOME             = ${HOME}"
	@echo "PWD              = ${PWD}"
	@echo "SHELL            = ${SHELL}"

help:
	@echo "Targets:"
	@echo "--------------------------------------------------------------------------------"
	@echo "  epr                - executes the main program to rename images"
	@echo "--------------------------------------------------------------------------------"
	@echo "  install            - installs required packages"
	@echo "  install_test       - installs required test packages"
	@echo "  install_dev        - installs required development packages"
	@echo "--------------------------------------------------------------------------------"
	@echo "  test               - runs test"
	@echo "  test_v             - runs test with verbose messaging"
	@echo "  test_ff            - runs test fast fail"
	@echo "  test_vff           - runs test fast fail with verbose messaging"
	@echo "  test_1 <file.class.test> - runs a single test"
	@echo "  coverage           - runs test, produces coverage and displays it"
	@echo "--------------------------------------------------------------------------------"
	@echo "  clean              - cleans some auto generated build files"
	@echo "--------------------------------------------------------------------------------"
	@echo "  sdist              - builds sdist for pypi"
	@echo "  sdist              - creates build"
	@echo "  wheel              - creates wheel build"
	@echo "  testpypi           - uploads build to testpypi"
	@echo "  pypi               - uploads build to pypi"
	@echo "--------------------------------------------------------------------------------"
	@echo "  settings           - outputs current settings"
	@echo "  help               - outputs this info"
