"""Main program for displaying ingredients list for shopping with the recipes liked"""

# Standard library imports
import sys

# Third party imports
from colorama import Fore, Style

# Local application imports
# from ingredients_input import IngredientsInput


def main():
    exit_code = 0
    try:
        pass
        # ingredient_list = get_ingredients()
        # ingredient_list = ['garlic', 'ginger', 'granny smith apple']
    except Exception as exception:
        print(Fore.RED + f"ERROR: executing exif image renamer")
        print(f"{exception}{Style.RESET_ALL}")
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
