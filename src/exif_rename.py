#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import os
import sys
# import asyncio

# Third party imports
from optparse import OptionParser, Values
# from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
# import exiftool

# Local application imports
from _version import __version__

class ExifRename:
    """ExifRename contains module to convert RAW images to DNG and rename them using exif meta data"""
    _args = None
    _options = None
    _current_dir = None

    def __init__(self, options:Values=None, args:list=None):
        self._options = options
        self._args = args


    def handle_options(self) -> None:
        """Handles user specified options and arguments"""
        usage_string = "usage: %prog [options]"
        version_string = "%prog version: " + Fore.GREEN + f"{__version__}{Style.RESET_ALL}"
        parser = OptionParser(usage=usage_string, version=version_string)
        parser.add_option(
            "-d",
            "--directory",
            action="store",
            dest="dir",
            default=".",
            help="directory, where images will be converted and renamed"
        )
        parser.add_option(
            "-v",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="verbose execution"
        )
        (self._options, self._args) = parser.parse_args()

        if len(self._args) != 0:
            parser.error("wrong number of arguments")

        if self._options.verbose:
            print(f"options: {self._options}")
            print(f"args: {self._args}")
            print(f"options.dir: {self._options.dir}")
            print(f"__version__: {__version__}")


    def move_rename_convert_images(self) -> None:
        self._change_to_image_dir()
        self._change_from_image_dir()


    def return_to_previous_state(self):
        self._change_from_image_dir()


    def _change_to_image_dir(self) -> None:
        if self._options.dir != ".":
            self._current_dir = os.getcwd()
            os.chdir(self._options.dir)
            if self._options.verbose:
                print(f"1. inside directory: {self._options.dir}")
                print(f"1. list dir: {os.listdir()}")


    def _change_from_image_dir(self) -> None:
        if self._current_dir is not None:
            os.chdir(self._current_dir)
            if self._options.verbose:
                print(f"2. inside directory: {self._current_dir}")
                print(f"2. list dir: {os.listdir()}")


    def _move_and_rename_files(self) -> None:
        pass


    def _convert_raw_files(self) -> None:
        pass


    def _read_image_dir(self):
        pass
        # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



def main():
    exit_code = 0
    exif_rename = ExifRename()

    try:
        exif_rename.handle_options()
        exif_rename.move_rename_convert_images()
    except Exception as exception:
        exif_rename.return_to_previous_state()
        print(Fore.RED + f"ERROR: executing exif image renamer")
        print(f"EXCEPTION: {exception}{Style.RESET_ALL}")
        exit_code = 1
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
