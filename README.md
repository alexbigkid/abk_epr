# ABK EXIF Picture Renamer ![Tests](https://github.com/alexbigkid/abk_epr/actions/workflows/pipeline.yml/badge.svg) [![codecov](https://codecov.io/gh/alexbigkid/abk_epr/branch/master/graph/badge.svg)](https://codecov.io/gh/alexbigkid/abk_epr)
Renames all image files in the folder according to image file exif metadata for easy ordering and archiving

[TOC]


## Prerequisites

| tool | description                                        |
| :--- | :------------------------------------------------- |
| make | tool to execute compile instructions from Makefile |
| uv   | python package manager                             |

- The project should work on MacOS and Linux and any other unix like system
- I haven't tried Windows, since I don't own a windows machine
- Stay tuned ... I am currently working on the single executable binary for MacOS, Linux and Windows


## Instructions for developers

On you terminal command line
- if you haven't installed <b>Homebrew</b> yet (password probably required):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- install <b>uv</b> - Python version and Python package manager tool with:
```bash
brew install uv
```
- clone <b>abk_bwp</b> repository:
```bash
git clone https://github.com/alexbigkid/abk_epr
cd abk_epr
```
- install Python dependencies
```bash
uv sync
```
- and run:
```bash
uv run epr
```


## Instructions for developers

| command                       | description                                        |
| :---------------------------- | :------------------------------------------------- |
| make help                     | to see all make rules                              |
| make epr                      | runs the program                                   |
| make quiet                    | runs the program in quiet mode                     |
| make log                      | runs with logging into a file: logs/abk_epr.log    |
| make install                  | installs required packages                         |
| make install_debug            | installs required packages for debugging problems  |
| make test                     | runs test                                          |
| make test_v                   | runs test with verbose messaging                   |
| make test_ff                  | runs test fast fail - fails on 1st error           |
| make test_vff                 | runs test fast fail - fails on 1st error verbosely |
| make test_1 <file.class.test> | runs a single test                                 |
| make coverage                 | runs test, produces coverage and displays it       |
| clean                         | cleans some auto generated build files             |
| sdist                         | builds sdist for pypi                              |
| sdist                         | creates build                                      |
| wheel                         | creates wheel build                                |
| testpypi                      | uploads build to testpypi                          |
| pypi                          | uploads build to pypi                              |
| settings                      | outputs current settings                           |


### App runs on:
- [x] MacOS Sequoia (local machine) / Python 3.13.3
- [ ] Linux Ubuntu 20.04  / Python 3.12.x
- [ ] Windows 10 / Python 3.12.x


### Pipeline Unit Tests ran on:
- [x] Linux latest / Python 3.12.x, 3.13.x
- [x] MacOS latest / Python 3.12.x, 3.131.x
- [x] Windows latest / Python 3.12.x, 3.13.x

:checkered_flag:
