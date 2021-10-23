#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import sys

# Third party imports
from optparse import OptionParser
import asyncio
from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
import exiftool

# Local application imports
# from ingredients_input import IngredientsInput

def handle_options():
    usage_string = "usage: %prog [options] [directory_name]"
    version_string = "%prog 1.0"
    parser = OptionParser(usage=usage_string, version=version_string)
    parser.add_option(
        "-d",
        "--directory",
        action="store",
        default=".",
        help=" directory name to convert and rename images"
    )
    (options, args) = parser.parse.args()

    if len(args) > 1:
        parser.error("wrong number of arguments")

    print(options)
    print(args)

def main():
    exit_code = 0
    handle_options()

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
