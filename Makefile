.PHONY:	upgrade_setuptools install install_dev install_nth test test_v test_ff test_vff settings help
.SILENT: epr coverage clean
EPR_HOME = src/abk_epr

# -----------------------------------------------------------------------------
# abk_epr Makefile rules
# -----------------------------------------------------------------------------
epr:
	echo "[ python ./src/abk_epr.py -d ./data/20230725_mixed_img -c ./src/logging.yaml -v ]"
	echo "------------------------------------------------------------------------------------"
	cd $(EPR_HOME) && python abk_epr.py -d ../data/20230725_mixed_img -c logging.yaml -v

log:
	cd $(EPR_HOME) && python abk_epr.py -d ../data/20230725_mixed_img -c logging.yaml -l -v

epr_clean:
	cd $(EPR_HOME) && rm -Rf ../data/20230725_mixed_img && cp -R ../data/20230725_mixed_img_backup ../data/20230725_mixed_img

# -----------------------------------------------------------------------------
# Dependency installation Makefile rules
# -----------------------------------------------------------------------------
install:
	uv sync

install_debug:
	uv pip install --group debug


# -----------------------------------------------------------------------------
# Running tests Makefile rules
# -----------------------------------------------------------------------------
test:
	uv run python -m unittest discover --start-directory tests

test_ff:
	uv run python -m unittest discover --start-directory tests --failfast

test_v:
	uv run python -m unittest discover --start-directory tests --verbose

test_vff:
	uv run python -m unittest discover --start-directory tests --verbose --failfast

%:
	@:

test_1:
	uv run python -m unittest "tests.$(filter-out $@,$(MAKECMDGOALS))"

coverage:
	uv run coverage run --source $(EPR_HOME) --omit ./tests/*,./$(EPR_HOME)/config/*  -m unittest discover --start-directory tests
	@echo
	uv run coverage report
	uv run coverage xml


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
	@echo "EPR_HOME         = $(EPR_HOME)"

help:
	@echo "Targets:"
	@echo "--------------------------------------------------------------------------------"
	@echo "  epr                - executes the main program to rename images"
	@echo "  quiet              - executes the abk_epr in quiet mode (no logs)"
	@echo "  log                - executes the abk_epr with logging into a file: logs/abk_epr.log"
	@echo "--------------------------------------------------------------------------------"
	@echo "  install            - installs required packages"
	@echo "  install_debug      - installs required debug packages"
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
