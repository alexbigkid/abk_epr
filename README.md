# :octocat: exif image renamer :octocat:
EXIF image renamer - renames all image files in the folder according to image file exif metadata for easy ordering and archiving


## Prerequisites
| tool   | description                                        |
| :----- | :------------------------------------------------- |
| make   | tool to execute compile instructions from Makefile |
| pip    | python package installer                           |
| python | python interpreter (3.9.4 was used)                |

- The project should work on MacOS and Linux and any other unix like system
- I haven't tried Windows, since I don't own a windows machine
- All required packages to run the app are in requirements.txt
- All require packages to run test are in requirements_dev.txt


*** In case the system is setup that python is linked to python version 2.* ***
*** and python3 is linked to version 3.*, please use the 2nd set of rules postfixed with 3 ***
*** on the command line execute "make help" to see all Makefile rules defined ***


## Instructions for users (if make tool is installed)
| command          | description                         |
| :--------------- | :---------------------------------- |
| make install     | installs needed python dependencies |
| make exif_rename | starts the program                  |


## Instructions for users (make tool is not available)
| command                                | description                         |
| :------------------------------------- | :---------------------------------- |
| pip install --user -r requirements.txt | installs needed python dependencies |
| python ./src/main.py                   | starts the program                  |



## Instructions for developers
| command           | description                                  |
| :---------------- | :------------------------------------------- |
| make help         | to see all make rules                        |
| make exif_rename  | executes the main program                    |
| make install      | installs required packages                   |
| make install_dev  | installs required development packages       |
| make test         | runs test                                    |
| make test_verbose | runs test with verbose messaging             |
| make coverage     | runs test, produces coverage and displays it |


#### Test ran on:
- [x] MacOS Big Sur (local machine and pipeline) / Python 3.8.9
- [ ] Linux Ubuntu 20.04 (pipeline machine) / Python 3.8.5
- [ ] Windows 10 (pipeline) / Python 3.7
- [ ] Raspberry Pi Zero W (via ssh) / Python 3.7.3


#### program tested running on:
- [x] MacOS Big Sur (local machine) / Python 3.9.4
- [ ] Linux Ubuntu 20.04  / Python 3.8.5
- [ ] Windows 10 (pipeline) / Python 3.7
- [ ] Raspberry Pi Zero W (via ssh) / Python 3.7.3


## API used
This project utilizes [Spoonacular API](https://spoonacular.com/food-api/docs) to get recipes from ingredient list. Following API are used:
- [Get recipes from ingredients API](https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients)
- [Get recipe price breakdown API](https://spoonacular.com/food-api/docs#Get-Recipe-Price-Breakdown-by-ID)


## Screenshot of functioning app
<!-- ![The screenshot](docs/running_app.jpg?raw=true "running app") -->

:checkered_flag:
