.PHONY:	upgrade_setuptools install install_dev test test_verbose exif_rename exif_rename3 settings help
.SILENT: exif_rename exif_rename3 coverage clean

EXIF_RENAME_DIR = src

# -----------------------------------------------------------------------------
# exif_rename Makefile rules
# -----------------------------------------------------------------------------
exif_rename:
	echo "[ python ./src/exif_rename.py -d ./data/20220101_sony_raw -c ./src/logging.yaml -v ]"
	echo "------------------------------------------------------------------------------------"
	python ./src/exif_rename.py -d ./data/20220101_sony_raw -c ./src/logging.yaml -v


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
	coverage run --source $(EXIF_RENAME_DIR) --omit ./tests/*,./$(EXIF_RENAME_DIR)/config/*  -m unittest discover --start-directory tests
	@echo
	coverage report
	coverage xml


# -----------------------------------------------------------------------------
# Clean up Makefile rules
# -----------------------------------------------------------------------------
clean:
	@echo "deleting log files:"
	@echo "___________________"
	ls -la *.log*
	rm *.log*

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
	@echo "--------------------------------------------------------------------------------"
	@echo "  exif_rename        - executes the main program"
	@echo "  install            - installs required packages"
	@echo "  install_dev        - installs required development packages"
	@echo "  test               - runs test"
	@echo "  test_verbose       - runs test with verbose messaging"
	@echo "--------------------------------------------------------------------------------"
	@echo "  coverage           - runs test, produces coverage and displays it"
	@echo "  settings           - outputs current settings"
	@echo "  help               - outputs this info"
