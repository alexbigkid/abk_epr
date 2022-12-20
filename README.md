# :octocat: abk_epr - exif picture renamer :octocat

EXIF picture renamer - renames all image files in the folder according to image file exif metadata for easy ordering and archiving

## Prerequisites

| tool   | description                                        |
| :----- | :------------------------------------------------- |
| make   | tool to execute compile instructions from Makefile |
| pip    | python package installer                           |
| python | python interpreter                                 |

- The project should work on MacOS and Linux and any other unix like system
- I haven't tried Windows, since I don't own a windows machine
- All required packages to run the app are in requirements.txt
- All require packages to run test are in requirements_dev.txt

***In case the system is setup that python is linked to python version 2.* ***
*** and python3 is linked to version 3.*, please use the 2nd set of rules postfixed with 3***
***on the command line execute "make help" to see all Makefile rules defined***

## Instructions for users (if make tool is installed)

| command      | description                         |
| :----------- | :---------------------------------- |
| make install | installs needed python dependencies |
| make abk_epr | runs the program                    |


## Instructions for developers

| command                       | description                                        |
| :---------------------------- | :------------------------------------------------- |
| make help                     | to see all make rules                              |
| make abk_epr                  | runs the program                                   |
| make install                  | installs required packages                         |
| make install_test             | installs required test packages                    |
| make install_dev              | installs required development packages             |
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

#### Test ran on

- [x] MacOS Ventura (local machine and pipeline) / Python 3.11.1
- [ ] Linux Ubuntu 20.04 (pipeline machine) / Python 3.8.5
- [ ] Windows 10 (pipeline) / Python 3.7
- [ ] Raspberry Pi Zero W (via ssh) / Python 3.7.3

#### program tested running on

- [x] MacOS Ventura (local machine) / Python 3.11.1
- [ ] Linux Ubuntu 20.04  / Python 3.8.5
- [ ] Windows 10 (pipeline) / Python 3.7
- [ ] Raspberry Pi Zero W (via ssh) / Python 3.7.3

<!-- ## Screenshot of functioning app -->
<!-- ![The screenshot](docs/running_app.jpg?raw=true "running app") -->

:checkered_flag:
